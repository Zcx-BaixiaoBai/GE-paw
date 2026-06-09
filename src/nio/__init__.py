"""Stub for matrix-nio client library used in tests."""
from __future__ import annotations

from typing import Any, Optional


class AsyncClient:
    """Stub `nio.AsyncClient`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.kwargs = kwargs
        self.homeserver = kwargs.get("homeserver", "")
        self.user = kwargs.get("user", "")
        self.device_id = kwargs.get("device_id", "")
        self.access_token = kwargs.get("access_token", "")
        self.rooms: dict = kwargs.get("rooms", {})

    async def login(self, *args: Any, **kwargs: Any) -> "LoginResponse":
        return LoginResponse(access_token="dummy", device_id="dummy")

    async def logout(self, *args: Any, **kwargs: Any) -> None:
        return None

    async def close(self) -> None:
        return None

    async def room_send(self, *args: Any, **kwargs: Any):
        return None

    async def sync(self, *args: Any, **kwargs: Any) -> Any:
        return None

    async def sync_forever(self, *args: Any, **kwargs: Any) -> None:
        return None

    async def whoami(self, *args: Any, **kwargs: Any) -> Any:
        return None

    async def upload(self, *args: Any, **kwargs: Any) -> Any:
        return None

    def add_event_callback(self, *args: Any, **kwargs: Any) -> None:
        return None

    def add_to_device_callback(self, *args: Any, **kwargs: Any) -> None:
        return None


class AsyncClientConfig:
    """Stub `nio.AsyncClientConfig`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class LoginResponse:
    """Stub `nio.LoginResponse`."""

    def __init__(self, access_token: str = "", device_id: str = "", *args, **kwargs) -> None:
        self.access_token = access_token
        self.device_id = device_id
        for k, v in kwargs.items():
            setattr(self, k, v)


class KeysUploadResponse:
    """Stub `nio.KeysUploadResponse`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class SyncResponse:
    """Stub `nio.SyncResponse`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class UploadResponse:
    """Stub `nio.UploadResponse`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class RoomSendResponse:
    """Stub `nio.RoomSendResponse`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class RoomSendError(Exception):
    """Stub for nio.RoomSendError."""

    def __init__(self, message: str = "", *args, **kwargs) -> None:
        super().__init__(message)
        self.message = message
        for k, v in kwargs.items():
            setattr(self, k, v)


class UploadError(Exception):
    """Stub for nio.UploadError."""

    def __init__(self, message: str = "", *args, **kwargs) -> None:
        super().__init__(message)
        self.message = message
        for k, v in kwargs.items():
            setattr(self, k, v)


class LocalProtocolError(Exception):
    """Stub `nio.LocalProtocolError`."""

    def __init__(self, message: str = "", *args, **kwargs) -> None:
        super().__init__(message)
        for k, v in kwargs.items():
            setattr(self, k, v)


class MatrixRoom:
    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


# --- Events -----------------------------------------------------------------

class _EventBase:
    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class RoomMessage(_EventBase):
    """Stub `nio.RoomMessage` event."""
    pass


class RoomMessageText(RoomMessage):
    pass


class RoomMessageMedia(RoomMessage):
    pass


class RoomMessageAudio(RoomMessage):
    pass


class RoomMessageFile(RoomMessage):
    pass


class RoomMessageImage(RoomMessage):
    pass


class RoomMessageVideo(RoomMessage):
    pass


class RoomEncryptedAudio(RoomMessage):
    pass


class RoomEncryptedFile(RoomMessage):
    pass


class RoomEncryptedImage(RoomMessage):
    pass


class RoomEncryptedVideo(RoomMessage):
    pass


class MegolmEvent(_EventBase):
    """Stub `nio.MegolmEvent`."""
    pass


class CallAnswer(MegolmEvent):
    pass


class CallHangup(MegolmEvent):
    pass


class CallInvite(MegolmEvent):
    pass


class CallCandidates(MegolmEvent):
    pass


class UnknownEvent(MegolmEvent):
    pass


class ToDeviceEvent(_EventBase):
    """Stub `nio.ToDeviceEvent`."""
    pass


class ToDeviceError(Exception):
    """Stub `nio.ToDeviceError`."""

    def __init__(self, message: str = "", *args, **kwargs) -> None:
        super().__init__(message)
        for k, v in kwargs.items():
            setattr(self, k, v)


# --- Key verification events -----------------------------------------------

class KeyVerificationEvent(_EventBase):
    pass


class KeyVerificationStart(KeyVerificationEvent):
    pass


class KeyVerificationCancel(KeyVerificationEvent):
    pass


class KeyVerificationKey(KeyVerificationEvent):
    pass


class KeyVerificationMac(KeyVerificationEvent):
    pass


class Api:
    """Stub for nio.Api."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class ErrorResponse:
    """Stub for nio.ErrorResponse."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


__all__ = [
    "Api",
    "AsyncClient",
    "AsyncClientConfig",
    "CallAnswer",
    "CallCandidates",
    "CallHangup",
    "CallInvite",
    "ErrorResponse",
    "KeyVerificationCancel",
    "KeyVerificationEvent",
    "KeyVerificationKey",
    "KeyVerificationMac",
    "KeyVerificationStart",
    "KeysUploadResponse",
    "LocalProtocolError",
    "LoginResponse",
    "MatrixRoom",
    "MegolmEvent",
    "RoomEncryptedAudio",
    "RoomEncryptedFile",
    "RoomEncryptedImage",
    "RoomEncryptedVideo",
    "RoomMessage",
    "RoomMessageAudio",
    "RoomMessageFile",
    "RoomMessageImage",
    "RoomMessageMedia",
    "RoomMessageText",
    "RoomMessageVideo",
    "RoomSendError",
    "RoomSendResponse",
    "SyncResponse",
    "ToDeviceError",
    "ToDeviceEvent",
    "UnknownEvent",
    "UploadError",
    "UploadResponse",
]
