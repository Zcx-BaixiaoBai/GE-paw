"""Stub: agentscope.formatter for gepaw test isolation.

The real agentscope package ships heavy formatter implementations.
For gepaw tests we only need the abstract base class plus the three
chat-formatter subclasses (``OpenAIChatFormatter``, ``AnthropicChatFormatter``,
``GeminiChatFormatter``) to exist and be importable so that subclassing and
``isinstance`` checks work in :mod:`gepaw.agents.model_factory`.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class FormatterBase(ABC):
    """Abstract base mirroring the real ``agentscope.formatter.FormatterBase``."""

    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    @abstractmethod
    async def _format(self, msgs: List[Any]) -> List[dict]:
        """Convert a list of ``Msg`` objects into provider payload dicts."""

    async def format(self, msgs: List[Any]) -> List[dict]:
        return await self._format(msgs)


class OpenAIChatFormatter(FormatterBase):
    """Stub for OpenAI Chat Completions formatter."""

    promote_tool_result_images: bool = False

    async def _format(self, msgs: List[Any]) -> List[dict]:  # pragma: no cover
        raise NotImplementedError


try:
    pass  # real AnthropicChatFormatter imports independently below
except Exception:  # pragma: no cover
    AnthropicChatFormatter = None  # type: ignore[assignment]


class AnthropicChatFormatter(FormatterBase):  # type: ignore[no-redef]
    """Stub for Anthropic Messages formatter."""

    async def _format(self, msgs: List[Any]) -> List[dict]:  # pragma: no cover
        raise NotImplementedError


class GeminiChatFormatter(FormatterBase):
    """Stub for Gemini formatter."""

    promote_tool_result_images: bool = False

    async def _format(self, msgs: List[Any]) -> List[dict]:  # pragma: no cover
        raise NotImplementedError


__all__ = [
    "FormatterBase",
    "OpenAIChatFormatter",
    "AnthropicChatFormatter",
    "GeminiChatFormatter",
]