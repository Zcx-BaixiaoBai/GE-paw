"""Console push store stub used by `ConsoleChannel`.

Stores the last few messages per session, so the HTTP `/console/chat`
endpoint (or any external consumer) can fetch recent console output.
"""
from __future__ import annotations

import asyncio
from collections import deque
from typing import Deque, Dict


_MAX_HISTORY = 200
_store: Dict[str, Deque[str]] = {}
_lock = asyncio.Lock()


async def append(session_id: str, text: str) -> None:
    """Append a text fragment to a session's push history."""
    if not session_id:
        return
    async with _lock:
        dq = _store.setdefault(session_id, deque(maxlen=_MAX_HISTORY))
        dq.append(text)


async def get(session_id: str) -> list:
    """Return all stored text fragments for `session_id`."""
    async with _lock:
        return list(_store.get(session_id, ()))


async def clear(session_id: str) -> None:
    async with _lock:
        _store.pop(session_id, None)


async def consume(session_id: str) -> list:
    """Return and clear the pending messages for `session_id`."""
    async with _lock:
        dq = _store.pop(session_id, None)
        return list(dq or [])


async def get_recent(session_id: str = "", limit: int = 50) -> list:
    """Return up to ``limit`` most recent messages for ``session_id``.
    If ``session_id`` is empty, return recent messages from ALL sessions."""
    async with _lock:
        if not session_id:
            combined: list = []
            for dq in _store.values():
                combined.extend(list(dq))
            return combined[-limit:]
        dq = _store.get(session_id, ())
        if not dq:
            return []
        return list(dq)[-limit:]


async def take(session_id: str, limit: int = 50) -> list:
    """Return up to ``limit`` messages and clear them for ``session_id``."""
    async with _lock:
        dq = _store.get(session_id)
        if not dq:
            return []
        items = list(dq)[-limit:]
        for _ in items:
            if dq:
                dq.popleft()
        return items


__all__ = ["append", "get", "clear", "consume", "get_recent", "take"]
