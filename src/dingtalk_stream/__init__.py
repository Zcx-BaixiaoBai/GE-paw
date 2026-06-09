"""Stub for dingtalk_stream SDK."""
from __future__ import annotations
from typing import Any


class ChatbotMessage:
    """Stub for `dingtalk_stream.ChatbotMessage`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def from_dict(cls, data: dict) -> "ChatbotMessage":
        return cls(**(data or {}))

    def to_dict(self) -> dict:
        return dict(self.__dict__)


class Credential:
    """Stub for `dingtalk_stream.Credential`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class DingTalkStreamClient:
    """Stub for `dingtalk_stream.DingTalkStreamClient`."""

    def __init__(self, credential: Any = None) -> None:
        self.credential = credential

    async def start(self) -> None:
        return None

    async def stop(self) -> None:
        return None

    def register_callback_handler(self, *args: Any, **kwargs: Any) -> None:
        return None


class CallbackMessage:
    """Stub for `dingtalk_stream.CallbackMessage`."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def from_dict(cls, data):
        return cls(**(data or {}))


class CallbackHandler:
    """Stub for `dingtalk_stream.CallbackHandler`."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class ChatbotHandler:
    """Stub for `dingtalk_stream.ChatbotHandler` base class."""

    def __init__(self) -> None:
        pass

    async def process(self, *args, **kwargs):
        return None

    def reply_text(self, *args, **kwargs):
        return None
