"""Stub for agentscope.agent._react_agent."""
from __future__ import annotations
from typing import Any, Optional


class ReActAgent:
    """Stub for `agentscope.agent._react_agent.ReActAgent`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    async def reply(self, *args: Any, **kwargs: Any) -> Any:
        return None

    async def a_reply(self, *args: Any, **kwargs: Any) -> Any:
        return None


class _MemoryMark:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
