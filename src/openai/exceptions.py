"""Stub exceptions for gepaw test isolation."""
from __future__ import annotations


class APIError(Exception):
    """Generic API error placeholder."""

    def __init__(self, message: str = "", **kwargs) -> None:
        super().__init__(message)
        for k, v in kwargs.items():
            setattr(self, k, v)