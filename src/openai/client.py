"""Stub AsyncOpenAI for gepaw test isolation."""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class AsyncOpenAI:
    """Minimal placeholder matching the real openai.AsyncOpenAI interface."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.api_key = api_key or ""
        self.base_url = base_url or ""
        self.kwargs = kwargs
        self.audio = self._AudioNamespace()

    class _AudioNamespace:
        async def transcriptions(self, **_kwargs: Any) -> Any:  # pragma: no cover
            raise NotImplementedError