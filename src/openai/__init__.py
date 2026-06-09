"""Stub: minimal openai client for gepaw test isolation."""
from .client import AsyncOpenAI
from .exceptions import APIError

__all__ = ["AsyncOpenAI", "APIError"]