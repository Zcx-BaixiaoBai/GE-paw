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


__all__ = ["append", "get", "clear", "consume"]
