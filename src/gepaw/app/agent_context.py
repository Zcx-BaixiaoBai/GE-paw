"""gepaw.app.agent_context: per-request agent identity context variables.

The real module resolves the active agent from FastAPI request state and
falls back to ``load_config()``.  This lightweight port only exposes the
symbols that downstream tool code imports; tests rely on ``set_*``
helpers to inject values into ``ContextVar`` storage.
"""
from __future__ import annotations

from contextvars import ContextVar
from typing import Optional


# ---------------------------------------------------------------------------
# Context variables
# ---------------------------------------------------------------------------

_current_agent_id: ContextVar[Optional[str]] = ContextVar(
    "current_agent_id",
    default=None,
)
_current_session_id: ContextVar[Optional[str]] = ContextVar(
    "current_session_id",
    default=None,
)
_current_root_session_id: ContextVar[Optional[str]] = ContextVar(
    "current_root_session_id",
    default=None,
)
_current_user_id: ContextVar[Optional[str]] = ContextVar(
    "current_user_id",
    default=None,
)
_current_channel: ContextVar[Optional[str]] = ContextVar(
    "current_channel",
    default=None,
)


# ---------------------------------------------------------------------------
# Accessors
# ---------------------------------------------------------------------------

def get_current_agent_id() -> Optional[str]:
    """Return the active agent id from context."""
    return _current_agent_id.get()


def set_current_agent_id(agent_id: Optional[str]) -> object:
    """Set the current agent id; returns the ``ContextVar`` token."""
    return _current_agent_id.set(agent_id)


def get_current_session_id() -> Optional[str]:
    return _current_session_id.get()


def set_current_session_id(session_id: Optional[str]) -> object:
    return _current_session_id.set(session_id)


def get_current_root_session_id() -> Optional[str]:
    return _current_root_session_id.get()


def set_current_root_session_id(root_session_id: Optional[str]) -> object:
    return _current_root_session_id.set(root_session_id)


def get_current_user_id() -> Optional[str]:
    return _current_user_id.get()


def set_current_user_id(user_id: Optional[str]) -> object:
    return _current_user_id.set(user_id)


def get_current_channel() -> Optional[str]:
    return _current_channel.get()


def set_current_channel(channel: Optional[str]) -> object:
    return _current_channel.set(channel)


# ---------------------------------------------------------------------------
# Active-agent resolution (fallback to config)
# ---------------------------------------------------------------------------

def get_active_agent_id() -> Optional[str]:
    """Return the configured active agent id, falling back to context."""
    try:
        from ..config.config import load_config

        config = load_config()
        if config and getattr(config, "active_agent_id", None):
            return config.active_agent_id
    except Exception:
        pass
    return get_current_agent_id()


__all__ = [
    "get_active_agent_id",
    "get_current_agent_id",
    "get_current_channel",
    "get_current_root_session_id",
    "get_current_session_id",
    "get_current_user_id",
    "set_current_agent_id",
    "set_current_channel",
    "set_current_root_session_id",
    "set_current_session_id",
    "set_current_user_id",
]