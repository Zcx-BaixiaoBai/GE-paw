"""In-chat slash command handler.

The full QwenPaw command handler covers /help, /load_history, /show_memory,
/start_proactive, /stop_proactive and so on. v0.1 only ships the ``/clear``
path that ``tests/unit/agents/test_command_handler.py`` exercises; the
stubs for the other commands remain in place as no-ops so import does not
break anything that references them by name.
"""
from __future__ import annotations

import logging
from typing import Any, Optional

from .message import Msg

logger = logging.getLogger(__name__)


class CommandHandler:
    """Dispatch chat-side slash commands for a single agent."""

    def __init__(self, agent_name: str, memory: Any) -> None:
        self.agent_name = agent_name
        self.memory = memory

    async def handle_command(self, command: str) -> Msg:
        """Dispatch a single slash command.

        Returns a ``Msg`` with ``metadata`` describing what the caller
        should do next (clear UI history, drop plan, ...). Unknown
        commands return an empty ``Msg`` so the chat UI can ignore them.
        """
        cmd = (command or "").strip().lower()
        if cmd in ("", "/"):
            return Msg(
                name=self.agent_name,
                role="assistant",
                content="",
                metadata={},
            )

        if cmd == "/clear":
            return await self._handle_clear()
        if cmd in ("/help", "/?"):
            return Msg(
                name=self.agent_name,
                role="assistant",
                content="",
                metadata={"help": True},
            )
        if cmd == "/load_history":
            return Msg(
                name=self.agent_name,
                role="assistant",
                content="",
                metadata={"load_history": True},
            )
        if cmd == "/show_memory":
            return Msg(
                name=self.agent_name,
                role="assistant",
                content="",
                metadata={"show_memory": True},
            )
        if cmd == "/start_proactive":
            return Msg(
                name=self.agent_name,
                role="assistant",
                content="",
                metadata={"start_proactive": True},
            )
        if cmd == "/stop_proactive":
            return Msg(
                name=self.agent_name,
                role="assistant",
                content="",
                metadata={"stop_proactive": True},
            )

        logger.warning("Unknown slash command: %s", command)
        return Msg(
            name=self.agent_name,
            role="assistant",
            content="",
            metadata={"unknown_command": command},
        )

    async def _handle_clear(self) -> Msg:
        memory = self.memory
        # ``clear_content`` is async on real memory managers; call it via
        # ``await`` when available. ``clear_compressed_summary`` is sync.
        clear_content = getattr(memory, "clear_content", None)
        if clear_content is not None:
            result = clear_content()
            if hasattr(result, "__await__"):
                await result
        clear_summary = getattr(memory, "clear_compressed_summary", None)
        if clear_summary is not None:
            clear_summary()
        return Msg(
            name=self.agent_name,
            role="assistant",
            content="",
            metadata={"clear_history": True, "clear_plan": True},
        )