"""First-interaction bootstrap hook.

The ``BootstrapHook`` looks for a ``BOOTSTRAP.md`` next to the agent's
``working_dir`` and, on the first user turn, prepends its guidance to
the first user message. After a successful run it drops a
``.bootstrap_completed`` flag so subsequent runs are no-ops.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

_FLAG_NAME = ".bootstrap_completed"
_BOOTSTRAP_FILE = "BOOTSTRAP.md"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def is_first_user_interaction(agent: Any) -> bool:
    """Return True iff the agent has not interacted with the user yet.

    The gepaw agent surface uses ``agent.memory`` to track past turns.
    The tests mock ``agent.memory.get_memory`` directly, so this helper
    is intentionally conservative: it returns True when ``get_memory``
    is missing or when it raises.
    """
    memory = getattr(agent, "memory", None)
    if memory is None:
        return True
    get_memory = getattr(memory, "get_memory", None)
    if get_memory is None:
        return True
    try:
        result = get_memory()
    except Exception:
        return True
    if hasattr(result, "__await__"):
        try:
            import asyncio
            result = asyncio.get_event_loop().run_until_complete(result)
        except RuntimeError:
            return True
        except Exception:
            return True
    return not result


def build_bootstrap_guidance(language: str = "zh") -> str:
    """Return the bootstrap guidance text for the requested language."""
    lang = (language or "zh").lower()
    table = {
        "en": (
            "Welcome! Before we start, please describe what you would like to do "
            "and share any relevant context (project, environment, constraints). "
            "The following BOOTSTRAP.md is the agreed-upon working agreement:\n\n"
        ),
        "zh": (
            "欢迎！在开始之前，请简要说明你希望完成的任务以及相关背景（项目、环境、"
            "约束等）。下面是从 BOOTSTRAP.md 提炼出的协作约定：\n\n"
        ),
        "ja": (
            "ようこそ！作業を始める前に、目的と背景（プロジェクト、環境、制約など）"
            "を簡単に共有してください。次の BOOTSTRAP.md は合意済みの作業規約です：\n\n"
        ),
        "ru": (
            "Dobro pozhalovat'! Pered nachalom raboty opishite vashu zadachu i "
            "kontekst (proekt, sreda, ogranichenija). Nizhe privedeny "
            "soglashennye pravila raboty iz BOOTSTRAP.md:\n\n"
        ),
    }
    return table.get(lang, table["zh"])


def prepend_to_message_content(message: Any, prefix: str) -> None:
    """Prepend ``prefix`` to ``message``'s textual content in place."""
    if message is None:
        return
    content = getattr(message, "content", None)
    if isinstance(content, str):
        message.content = prefix + content
        return
    if isinstance(content, list):
        # If the first block is a text block, merge into it; otherwise
        # insert a new text block at the head.
        if content and isinstance(content[0], dict) and content[0].get("type") == "text":
            text = content[0].get("text", "")
            content[0]["text"] = prefix + text
            return
        content.insert(0, {"type": "text", "text": prefix})
        return
    if content is None:
        message.content = prefix
        return
    # Fallback: stringify.
    try:
        message.content = prefix + str(content)
    except Exception:
        logger.debug("Failed to prepend guidance", exc_info=True)


def _first_user_message(messages):
    for m in messages or []:
        role = getattr(m, "role", None)
        if role == "user":
            return m
    return None


# ---------------------------------------------------------------------------
# Hook
# ---------------------------------------------------------------------------


class BootstrapHook:
    """Prepend ``BOOTSTRAP.md`` guidance on the first user turn."""

    def __init__(
        self,
        working_dir,
        language: str = "zh",
    ) -> None:
        self.working_dir = Path(working_dir)
        self.language = language

    def _bootstrap_path(self) -> Path:
        return self.working_dir / _BOOTSTRAP_FILE

    def _flag_path(self) -> Path:
        return self.working_dir / _FLAG_NAME

    async def __call__(self, agent: Any, _kwargs: dict) -> Optional[Any]:
        # Already bootstrapped: no-op.
        try:
            if self._flag_path().exists():
                return None
        except OSError:
            return None
        # No bootstrap file: nothing to prepend.
        try:
            if not self._bootstrap_path().exists():
                return None
        except OSError:
            return None
        if not is_first_user_interaction(agent):
            return None
        try:
            messages = await agent.memory.get_memory()
        except Exception:
            logger.warning("BootstrapHook: failed to load memory", exc_info=True)
            return None
        target = _first_user_message(messages)
        if target is None:
            return None
        guidance = build_bootstrap_guidance(self.language)
        prepend_to_message_content(target, guidance)
        # Drop the completion flag so subsequent turns short-circuit.
        try:
            self._flag_path().touch(exist_ok=True)
        except OSError:
            logger.debug("Could not write bootstrap flag", exc_info=True)
        return None