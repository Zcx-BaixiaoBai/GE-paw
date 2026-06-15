# -*- coding: utf-8 -*-
"""Model wrapper that records token usage from LLM responses."""

from datetime import date, datetime, timezone
from typing import Any, AsyncGenerator, Literal, Type

from agentscope.model import ChatModelBase
from agentscope.model._model_response import ChatResponse
from agentscope.model._model_usage import ChatUsage
from pydantic import BaseModel

from .buffer import _UsageEvent
from .manager import get_token_usage_manager

def _try_gateway_check(messages: list[dict], response_text: str = "") -> None:
    """????????????????"""
    try:
        from ..app.agent_context import get_current_session_id, get_current_agent_id
        from ..app.db import session_scope
        from ..app.gateway.service import GatewayService
        from ..config.config import load_agent_config

        session_id = get_current_session_id() or ""
        agent_id = get_current_agent_id()
        org_id = "default"
        if agent_id:
            try:
                cfg = load_agent_config(agent_id)
                org_id = getattr(cfg, "org_id", "default") or "default"
            except Exception:
                pass

        with session_scope() as db:
            svc = GatewayService(db, org_id=org_id)
            req_result = svc.check_messages(messages, session_id=session_id)
            if req_result.blocked:
                raise ValueError(
                    "???????????: " + ", ".join(h.keyword for h in req_result.hits)
                )
            if response_text:
                resp_result = svc.check_response(response_text, session_id=session_id)
                if resp_result.blocked:
                    raise ValueError(
                        "???????????: " + ", ".join(h.keyword for h in resp_result.hits)
                    )
    except ValueError:
        raise
    except Exception:
        pass  # ?????????????



class TokenRecordingModelWrapper(ChatModelBase):

    async def stream(self, *args, **kwargs):
        """Stub `stream` to satisfy the abstract base."""
        yield None

    """Wraps a ChatModelBase to record token usage on each call."""

    _usage_by_session: dict[str, dict[str, Any]] = {}

    def __init__(self, provider_id: str, model: ChatModelBase) -> None:
        super().__init__(
            model_name=getattr(model, "model_name", "unknown"),
            stream=getattr(model, "stream", True),
        )
        self._model = model
        self._provider_id = provider_id

    def _record_usage(self, usage: ChatUsage | None) -> None:
        """Enqueue a usage event synchronously 鈥?never blocks the caller."""
        if usage is None:
            return
        pt = getattr(usage, "input_tokens", 0) or 0
        ct = getattr(usage, "output_tokens", 0) or 0
        if pt <= 0 and ct <= 0:
            return

        event = _UsageEvent(
            provider_id=self._provider_id,
            model_name=self.model_name,
            prompt_tokens=pt,
            completion_tokens=ct,
            date_str=date.today().isoformat(),
            now_iso=datetime.now(tz=timezone.utc).isoformat(
                timespec="seconds",
            ),
        )
        # Fire-and-forget: synchronous put_nowait, ~100 ns, no await needed.
        get_token_usage_manager().enqueue(event)

        usage_data = {
            "provider_id": self._provider_id,
            "model_name": self.model_name,
            "prompt_tokens": pt,
            "completion_tokens": ct,
            "total_tokens": pt + ct,
        }
        self._store_usage(usage_data)

    @classmethod
    def pop_usage_for_session(cls, session_id: str) -> dict[str, Any] | None:
        return cls._usage_by_session.pop(session_id, None)

    def _store_usage(self, usage: dict[str, Any] | None) -> None:
        from ..app.agent_context import get_current_session_id

        session_id = get_current_session_id()
        if session_id and usage:
            TokenRecordingModelWrapper._usage_by_session[session_id] = usage

    async def __call__(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        tool_choice: Literal["auto", "none", "required"] | str | None = None,
        structured_model: Type[BaseModel] | None = None,
        **kwargs: Any,
    ) -> ChatResponse | AsyncGenerator[ChatResponse, None]:
        # Fix: Omit tool_choice="auto" for vLLM compatibility
        # vLLM without --enable-auto-tool-choice will reject requests when
        # tool_choice="auto" is present, even if tools are provided.
        # By omitting tool_choice when it's "auto", we bypass the check
        # while keeping tools available for correct tool calling behavior.
        if tool_choice == "auto":
            tool_choice = None

        # Gateway content filter check
        _try_gateway_check(messages)

        result = await self._model(
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            structured_model=structured_model,
            **kwargs,
        )

        if isinstance(result, AsyncGenerator):
            return self._wrap_stream(result)
        self._record_usage(getattr(result, "usage", None))
        return result

    async def _wrap_stream(
        self,
        stream: AsyncGenerator[ChatResponse, None],
    ) -> AsyncGenerator[ChatResponse, None]:
        last_usage: ChatUsage | None = None
        async for chunk in stream:
            if getattr(chunk, "usage", None) is not None:
                last_usage = chunk.usage
            yield chunk
        self._record_usage(last_usage)



async def stream(self, *args, **kwargs):
    """Stub `stream` to satisfy the abstract base."""
    yield None

def record_usage(
    db = None,
    *,
    org_id: str = "",
    model: str = "",
    provider_id: str = "",
    model_name: str = "",
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    cache_read_tokens: int = 0,
    cache_write_tokens: int = 0,
    cost_cents: float = 0.0,
    session_id = "",
    user_id = None,
    agent_id: str = "",
    raw: dict = None,
    commit: bool = True,
) -> int:
    """Convenience wrapper to record a usage event via the manager.

    Supports two call shapes:

    1. New style (with ``db``) -- inserts a row directly and returns its id.
    2. Legacy style (no ``db``) -- enqueues an event on the background
       manager for fire-and-forget recording.
    """
    if not model_name and model:
        model_name = model
    if not provider_id and model:
        provider_id = model

    if db is not None:
        try:
            from ..models.assistant import TokenUsageLog
        except Exception:
            TokenUsageLog = None  # type: ignore[assignment]
        if TokenUsageLog is None:
            return 0
        # Auto-compute cost_cents when caller did not pass one.
        if not cost_cents and model_name:
            try:
                from .cost_table import compute_cost_cents
                cost_cents = compute_cost_cents(
                    model_name,
                    int(prompt_tokens or 0),
                    int(completion_tokens or 0),
                )
            except Exception:
                cost_cents = 0
        # model_name is the canonical model field; provider_id is ignored here.
        kwargs = {
            "org_id": org_id,
            "user_id": user_id,
            "session_id": str(session_id or "") or None,
            "model": model_name or "",
            "prompt_tokens": int(prompt_tokens or 0),
            "completion_tokens": int(completion_tokens or 0),
            "total_tokens": int(prompt_tokens or 0) + int(completion_tokens or 0),
            "cost_cents": int(cost_cents or 0),
        }
        # Filter to columns the table actually has.
        valid = {k: v for k, v in kwargs.items() if k in TokenUsageLog.__table__.columns}
        row = TokenUsageLog(**valid)
        db.add(row)
        if commit:
            try:
                db.flush()
            except Exception:
                pass
        return getattr(row, "id", 0) or 0

    from .manager import get_token_usage_manager

def _try_gateway_check(messages: list[dict], response_text: str = "") -> None:
    """????????????????"""
    try:
        from ..app.agent_context import get_current_session_id, get_current_agent_id
        from ..app.db import session_scope
        from ..app.gateway.service import GatewayService
        from ..config.config import load_agent_config

        session_id = get_current_session_id() or ""
        agent_id = get_current_agent_id()
        org_id = "default"
        if agent_id:
            try:
                cfg = load_agent_config(agent_id)
                org_id = getattr(cfg, "org_id", "default") or "default"
            except Exception:
                pass

        with session_scope() as db:
            svc = GatewayService(db, org_id=org_id)
            req_result = svc.check_messages(messages, session_id=session_id)
            if req_result.blocked:
                raise ValueError(
                    "???????????: " + ", ".join(h.keyword for h in req_result.hits)
                )
            if response_text:
                resp_result = svc.check_response(response_text, session_id=session_id)
                if resp_result.blocked:
                    raise ValueError(
                        "???????????: " + ", ".join(h.keyword for h in resp_result.hits)
                    )
    except ValueError:
        raise
    except Exception:
        pass  # ?????????????

    manager = get_token_usage_manager()
    manager.enqueue(
        provider_id=provider_id or model_name,
        model_name=model_name,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        cache_read_tokens=cache_read_tokens,
        cache_write_tokens=cache_write_tokens,
        cost_cents=cost_cents,
        session_id=str(session_id or ""),
        user_id=str(user_id) if user_id is not None else "",
        agent_id=agent_id or "",
        raw=raw or {},
    )
    return 0

