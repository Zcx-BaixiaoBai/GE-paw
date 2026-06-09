"""Stub ChatModelBase for gepaw test isolation."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Dict, List, Optional, Union


class ChatModelBase(ABC):
    """Minimal placeholder matching the real agentscope interface."""

    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.model_name = model_name
        self.api_key = api_key or ""
        self.base_url = base_url or ""
        self.kwargs = kwargs

    @abstractmethod
    async def __call__(  # type: ignore[no-untyped-def]
        self,
        messages: List[Any],
        **kwargs: Any,
    ) -> Any:
        ...

    @abstractmethod
    async def stream(  # type: ignore[no-untyped-def]
        self,
        messages: List[Any],
        **kwargs: Any,
    ) -> AsyncIterator[Any]:
        ...