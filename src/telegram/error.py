"""Stub for telegram.error."""


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
