"""Stub for telegram.ext."""


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
