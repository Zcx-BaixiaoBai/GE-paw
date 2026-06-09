"""Stub for nio.responses."""
from __future__ import annotations
from typing import Any


class _BaseResponse:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self) -> str:
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'{type(self).__name__}({attrs})'


class WhoamiResponse(_BaseResponse):
    pass


class JoinedMembersResponse(_BaseResponse):
    pass


class RoomGetStateEventResponse(_BaseResponse):
    pass


class SyncError(Exception):
    """Stub for nio.responses.SyncError."""

    def __init__(self, message: str = '', *args, **kwargs) -> None:
        super().__init__(message)
        self.message = message
        for k, v in kwargs.items():
            setattr(self, k, v)
