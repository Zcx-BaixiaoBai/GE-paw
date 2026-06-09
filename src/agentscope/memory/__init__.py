"""Stub: agentscope.memory for gepaw test isolation."""
from __future__ import annotations

from typing import Any, Dict, List


class InMemoryMemory:
    """Stub for agentscope ``InMemoryMemory``."""

    def __init__(self) -> None:
        self._entries: List[Dict[str, Any]] = []

    def add(self, *args, **kwargs) -> None:
        self._entries.append({"args": args, "kwargs": kwargs})

    def get_memory(self, *args, **kwargs):
        return self._entries

    async def search(self, *args, **kwargs):
        return self._entries


__all__ = ["InMemoryMemory"]