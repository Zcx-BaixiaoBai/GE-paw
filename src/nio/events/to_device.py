"""Stub for nio.events.to_device."""
from __future__ import annotations
from typing import Any


class _ToDeviceBase:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class RoomKeyRequest(_ToDeviceBase):
    pass


class RoomKeyRequestCancellation(_ToDeviceBase):
    pass
