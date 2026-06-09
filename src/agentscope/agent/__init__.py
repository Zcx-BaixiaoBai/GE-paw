"""Stub: agentscope.agent for gepaw test isolation."""
from __future__ import annotations

from typing import Any


class ReActAgent:
    """Stub ReActAgent matching the upstream agent surface."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._state: dict = {"args": args, "kwargs": kwargs}

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    async def reply(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


__all__ = ["ReActAgent"]