"""Stub gepaw.agents.prompt module for test isolation.

The real ``gepaw.agents.prompt`` module centralises per-agent model
metadata access.  This stub only defines the symbols that downstream
tool modules import; tests patch individual functions as needed.
"""
from __future__ import annotations

from typing import Any, Optional, Tuple


def _get_active_model_info() -> Tuple[Optional[Any], Optional[Any]]:
    """Return ``(model_info, agent_id)`` for the active model.

    Tests patch this symbol. The stub returns ``(None, None)`` so that
    defensive tool code that calls it without patching gets the
    "no model info" branch.
    """
    return None, None


def get_active_model_supports_multimodal() -> bool:
    """Whether the active model advertises multimodal support."""
    return True


def get_active_model_multimodal_raw() -> Optional[bool]:
    """Raw multimodal flag (None when unknown)."""
    return None


__all__ = [
    "_get_active_model_info",
    "get_active_model_multimodal_raw",
    "get_active_model_supports_multimodal",
]