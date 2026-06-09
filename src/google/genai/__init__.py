"""Stub google.genai package for gepaw test isolation."""
from . import errors, types

__all__ = ["errors", "types", "Client"]

from typing import Any, Optional


class Client:
    """Placeholder for google.genai.Client."""

    def __init__(self, *, api_key: Optional[str] = None, **kwargs: Any) -> None:
        self.api_key = api_key or ""
        self.kwargs = kwargs

    class _ModelsNamespace:
        async def generate_content(self, **_kwargs: Any) -> Any:  # pragma: no cover
            raise NotImplementedError

    @property
    def models(self) -> "Client._ModelsNamespace":
        return self._ModelsNamespace()
