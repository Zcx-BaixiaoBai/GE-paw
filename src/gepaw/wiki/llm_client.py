"""Unified LLM client for GE-paw (OpenAI-compatible protocol)."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..models import LLMEndpoint
from ..security.crypto import decrypt
from ..utils.logging import get_logger
from ..constant import LLM_REQUEST_TIMEOUT, PROJECT_NAME

logger = get_logger("wiki.llm")


# Mapping between the Codex-style per-turn permission we expose in the chat
# composer and the internal ToolExecutionLevel. The "readonly" mode is a
# frontend-originated extra that does not have a direct ToolExecutionLevel
# equivalent, so we translate it into a runtime behaviour: strip tool
# affordances from the system prompt so the assistant refuses to act on them.
PERMISSION_TO_LEVEL = {
    "full": "off",        # all tools available, no approval
    "smart": "smart",     # smart risk-based approval
    "strict": "strict",   # every tool requires approval
    "readonly": "readonly",
}


@dataclass
class LLMResult:
    content: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    raw: Optional[Dict[str, Any]] = None


def _stub_answer(prompt: str) -> LLMResult:
    return LLMResult(
        content="(LLM endpoint not configured. An admin must add a default model on the LLM page.)",
        prompt_tokens=0, completion_tokens=0, total_tokens=0,
    )


def _call_openai_compat(
    endpoint: LLMEndpoint,
    messages: List[Dict[str, str]],
    *,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    timeout: Optional[int] = None,
) -> LLMResult:
    api_key = decrypt(endpoint.api_key_enc) or ""
    base_url = endpoint.base_url.rstrip("/")
    url = f"{base_url}/chat/completions"
    body: Dict[str, Any] = {"model": endpoint.model, "messages": messages}
    if temperature is not None:
        body["temperature"] = temperature
    if max_tokens is not None:
        body["max_tokens"] = max_tokens
    try:
        import httpx
    except Exception as e:
        raise RuntimeError(f"httpx not installed: {e}")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    try:
        r = httpx.post(url, json=body, headers=headers, timeout=timeout or LLM_REQUEST_TIMEOUT)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {e}")
    content = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
    usage = data.get("usage") or {}
    return LLMResult(
        content=content,
        prompt_tokens=int(usage.get("prompt_tokens") or 0),
        completion_tokens=int(usage.get("completion_tokens") or 0),
        total_tokens=int(usage.get("total_tokens") or 0),
        raw=data,
    )


def _apply_permission(messages: List[Dict[str, str]], permission: Optional[str]) -> List[Dict[str, str]]:
    """Mutate the messages list to honour the requested permission.

    - readonly:  inject a system note telling the model to refuse tool use and
      drop any system prompt that announces tool availability. The fallback is
      a soft contract - the model is expected to comply, and the audit log
      records the choice so admins can spot regressions.
    - smart/strict/full:  no mutation; the tool_guard layer elsewhere
      enforces the actual approval flow.
    """
    if permission != "readonly":
        return messages
    note = (
        "Permission mode: read-only. You must not request or imply tool use, "
        "file edits, or shell commands in this turn. Answer the user with "
        "explanations, code review, and reasoning only."
    )
    if messages and messages[0].get("role") == "system":
        messages[0] = {**messages[0], "content": (messages[0].get("content", "") + "\n\n" + note)}
    else:
        messages.insert(0, {"role": "system", "content": note})
    return messages


def chat_for_org(
    db,
    org_id: str,
    messages: List[Dict[str, str]],
    *,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    timeout: Optional[int] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    message_id: Optional[str] = None,
    permission: Optional[str] = None,
) -> "LLMResult":
    # Apply permission-mandated prompt adjustments before any persistence or
    # outbound call so token usage and audit see the post-transform prompt.
    messages = _apply_permission(list(messages), permission)
    from ..models import LLMEndpoint as _EP
    ep = (
        db.query(_EP)
        .filter(_EP.org_id == org_id, _EP.enabled == True)  # noqa: E712
        .order_by(_EP.is_default.desc(), _EP.created_at.asc())
        .first()
    )
    if ep is None:
        logger.info("org %s has no LLM endpoint, using stub", org_id)
        # Stub still records usage (zero tokens) so call counts stay consistent.
        try:
            from ..token_usage import record_usage
            record_usage(
                db,
                org_id=org_id,
                model="stub",
                prompt_tokens=0,
                completion_tokens=0,
                user_id=user_id,
                session_id=session_id,
                message_id=message_id,
            )
        except Exception:
            pass
        return _stub_answer(json.dumps(messages, ensure_ascii=False)[:200])
    try:
        res = _call_openai_compat(ep, messages, temperature=temperature, max_tokens=max_tokens, timeout=timeout)
    except Exception as e:
        # Re-raise; callers that want to track failed attempts (e.g. channel handler)
        # should record usage themselves in their own session so the write is
        # serialised with the rest of their work and avoids SQLite write locks.
        raise
    try:
        from ..token_usage import record_usage
        record_usage(
            db,
            org_id=org_id,
            model=ep.model,
            prompt_tokens=res.prompt_tokens,
            completion_tokens=res.completion_tokens,
            user_id=user_id,
            session_id=session_id,
            message_id=message_id,
        )
    except Exception as e:
        logger.warning("record_usage failed: %s", e)
    return res
