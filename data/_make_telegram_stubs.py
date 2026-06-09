import os
root = 'src'

# telegram
p = os.path.join(root, 'telegram')
os.makedirs(os.path.join(p, 'ext'), exist_ok=True)
open(os.path.join(p, '__init__.py'), 'w', encoding='utf-8').write('''"""Stub for python-telegram-bot library."""
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
''')

# telegram.constants
open(os.path.join(p, 'constants.py'), 'w', encoding='utf-8').write('''"""Stub for telegram.constants."""
from __future__ import annotations


class _Const:
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name


class ParseMode:
    MARKDOWN = _Const('MarkdownV2')
    MARKDOWN_V2 = _Const('MarkdownV2')
    HTML = _Const('HTML')
    PLAIN = _Const('')
''')

# telegram.error
open(os.path.join(p, 'error.py'), 'w', encoding='utf-8').write('''"""Stub for telegram.error."""


class TelegramError(Exception):
    """Stub for `telegram.error.TelegramError`."""


class BadRequest(TelegramError):
    pass


class Forbidden(TelegramError):
    pass


class InvalidToken(TelegramError):
    pass


class NetworkError(TelegramError):
    pass


class RetryAfter(TelegramError):
    def __init__(self, retry_after: float = 0, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.retry_after = retry_after


class TimedOut(TelegramError):
    pass


class ChatMigrated(TelegramError):
    pass
''')

# telegram.ext
open(os.path.join(p, 'ext', '__init__.py'), 'w', encoding='utf-8').write('''"""Stub for telegram.ext."""


class Application:
    @classmethod
    def builder(cls):
        return _Builder()

    async def initialize(self):
        return None

    async def start(self):
        return None

    async def stop(self):
        return None

    async def shutdown(self):
        return None

    async def process_update(self, *args, **kwargs):
        return None

    def add_handler(self, *args, **kwargs):
        return None

    def add_error_handler(self, *args, **kwargs):
        return None

    async def bot_send_message(self, *args, **kwargs):
        return None

    async def bot_set_my_commands(self, *args, **kwargs):
        return None

    bot = None


class _Builder:
    def token(self, token):
        self._token = token
        return self

    def get_updates_read_timeout(self, t):
        return self

    def get_updates_connect_timeout(self, t):
        return self

    def get_updates_pool_timeout(self, t):
        return self

    def get_updates_write_timeout(self, t):
        return self

    def proxy(self, url):
        return self

    def connection_pool_size(self, n):
        return self

    def read_timeout(self, t):
        return self

    def write_timeout(self, t):
        return self

    def connect_timeout(self, t):
        return self

    def pool_timeout(self, t):
        return self

    def build(self):
        return Application()


class CallbackQueryHandler:
    def __init__(self, callback=None, *args, **kwargs):
        self.callback = callback


class MessageHandler:
    def __init__(self, callback=None, filters=None, *args, **kwargs):
        self.callback = callback
        self.filters = filters


class CommandHandler:
    def __init__(self, command=None, callback=None, *args, **kwargs):
        self.command = command
        self.callback = callback


class ContextTypes:
    DEFAULT_TYPE = object


class _Filter:
    def __init__(self, name: str = ''):
        self.name = name

    def __call__(self, *args, **kwargs):
        return self

    def __or__(self, other):
        return self

    def __and__(self, other):
        return self

    def __invert__(self):
        return self


class _Filters:
    TEXT = _Filter('TEXT')
    PHOTO = _Filter('PHOTO')
    VIDEO = _Filter('VIDEO')
    AUDIO = _Filter('AUDIO')
    VOICE = _Filter('VOICE')
    DOCUMENT = _Filter('DOCUMENT')
    COMMAND = _Filter('COMMAND')
    ALL = _Filter('ALL')

    def __getattr__(self, name):
        return _Filter(name)


filters = _Filters()
''')

print('created telegram stubs')
