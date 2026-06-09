"""Stub AsyncAnthropic for gepaw test isolation."""
from __future__ import annotations

from typing import Any, Optional


class AsyncAnthropic:
    """Minimal placeholder matching anthropic.AsyncAnthropic."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.api_key = api_key or ""
        self.base_url = base_url or ""
        self.kwargs = kwargs

    class _MessagesNamespace:
        async def create(self, **_kwargs: Any) -> Any:  # pragma: no cover
            raise NotImplementedError

    @property
    def messages(self) -> "AsyncAnthropic._MessagesNamespace":
        return self._MessagesNamespace()