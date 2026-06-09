"""Access control for incoming channel messages.

v1 policy: every channel message is allowed. The hook is in place so a future
admin setting (e.g. an allowlist of external_user_ids) can be added without
touching the manager.
"""
from __future__ import annotations

from typing import Any, Dict

from .base import IncomingMessage


def is_allowed(msg: IncomingMessage, *, account: Dict[str, Any]) -> bool:
    return True


__all__ = ["is_allowed"]
