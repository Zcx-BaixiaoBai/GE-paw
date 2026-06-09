"""Stub AnthropicChatModel for gepaw test isolation."""
from __future__ import annotations

from typing import Any, AsyncIterator, List, Optional

from .chat_model_base import ChatModelBase


class AnthropicChatModel(ChatModelBase):
    """Placeholder for the real Anthropic chat model."""

    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            **kwargs,
        )

    async def __call__(  # type: ignore[no-untyped-def]
        self,
        messages: List[Any],
        **kwargs: Any,
    ) -> Any:
        raise NotImplementedError

    async def stream(  # type: ignore[no-untyped-def]
        self,
        messages: List[Any],
        **kwargs: Any,
    ) -> AsyncIterator[Any]:
        raise NotImplementedError
        yield  # pragma: no cover