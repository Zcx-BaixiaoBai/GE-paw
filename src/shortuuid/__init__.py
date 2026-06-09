"""Stub shortuuid for gepaw test isolation."""
from __future__ import annotations

import uuid as _uuid


def uuid() -> str:
    """Return a short unique id (22 chars)."""
    return _uuid.uuid4().hex[:22]


def random(length: int = 22) -> str:
    """Return a short unique id of *length* characters."""
    return _uuid.uuid4().hex[:length]