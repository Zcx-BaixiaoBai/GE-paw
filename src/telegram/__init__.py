"""Stub for python-telegram-bot library."""
from __future__ import annotations
from typing import Any


class BotCommand:
    def __init__(self, command: str = '', description: str = '') -> None:
        self.command = command
        self.description = description


class Update:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class Message:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class User:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class Chat:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class CallbackQuery:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class InlineKeyboardButton:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard=None, *args: Any, **kwargs: Any) -> None:
        self.inline_keyboard = inline_keyboard or []


class InputFile:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
