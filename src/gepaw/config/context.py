"""Context variables for per-agent state.

Workspace directory and similar per-request values are passed
through :mod:`contextvars` so multi-agent code can resolve
``gepaw.config.context.get_current_workspace_dir()`` to the right
agent without explicit threading.
"""
from __future__ import annotations

from contextvars import ContextVar
from pathlib import Path
from typing import Optional


current_workspace_dir: ContextVar[Optional[Path]] = ContextVar(
    "current_workspace_dir",
    default=None,
)


def get_current_workspace_dir() -> Optional[Path]:
    """Return the current agent's workspace directory, or ``None``."""
    return current_workspace_dir.get()


def set_current_workspace_dir(workspace_dir: Optional[Path]) -> object:
    """Set the current agent's workspace directory.

    Returns the :class:`contextvars.Token` so callers can restore the
    previous value if needed.
    """
    return current_workspace_dir.set(workspace_dir)


current_recent_max_bytes: ContextVar[Optional[int]] = ContextVar(
    "current_recent_max_bytes",
    default=None,
)


def get_current_recent_max_bytes() -> Optional[int]:
    return current_recent_max_bytes.get()


def set_current_recent_max_bytes(value: Optional[int]) -> object:
    return current_recent_max_bytes.set(value)