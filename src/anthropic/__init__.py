"""Stub: anthropic for gepaw test isolation."""
from ._client import AsyncAnthropic


class APIError(Exception):
    """Placeholder matching the real anthropic library exception type."""


class APIStatusError(APIError):
    """Raised for non-2xx responses from the Anthropic API."""

    def __init__(self, message="", response=None, body=None):
        super().__init__(message)
        self.response = response
        self.body = body


__all__ = ["AsyncAnthropic", "APIError", "APIStatusError"]
