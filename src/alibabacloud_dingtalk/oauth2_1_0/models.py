"""Stub for alibabacloud_dingtalk models (generic)."""
from __future__ import annotations
from typing import Any


class _Stub:
    """Generic stub class that accepts any keyword args as attributes."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


def __getattr__(name: str) -> Any:
    """Return a fresh stub class for any requested symbol."""
    return _Stub
