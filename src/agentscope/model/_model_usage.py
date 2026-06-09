"""Stub for agentscope.model._model_usage."""
from __future__ import annotations
from typing import Any


class ModelUsage:
    """Stub ModelUsage class."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class ChatUsage:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class _ModelUsage:
    pass
