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
# Per-agent shell command configuration overrides.
current_shell_command_executable: ContextVar[Optional[str]] = ContextVar(
    "current_shell_command_executable",
    default=None,
)
current_shell_command_timeout: ContextVar[Optional[int]] = ContextVar(
    "current_shell_command_timeout",
    default=None,
)


def get_current_shell_command_executable() -> Optional[str]:
    """Return the current agent's shell executable override, or ``None``."""
    return current_shell_command_executable.get()


def set_current_shell_command_executable(
    value: Optional[str],
) -> object:
    return current_shell_command_executable.set(value)


def get_current_shell_command_timeout() -> Optional[int]:
    """Return the current agent's shell command timeout (seconds)."""
    return current_shell_command_timeout.get()


def set_current_shell_command_timeout(value: Optional[int]) -> object:
    return current_shell_command_timeout.set(value)