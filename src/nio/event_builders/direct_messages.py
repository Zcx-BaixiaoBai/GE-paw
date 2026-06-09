"""Stub for nio.event_builders.direct_messages."""
from __future__ import annotations
from typing import Any


class ToDeviceMessage:
    """Stub `nio.event_builders.direct_messages.ToDeviceMessage`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def as_dict(self) -> dict:
        return dict(self.__dict__)
