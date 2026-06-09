"""Stub for mcp.client.streamable_http."""
from __future__ import annotations
from typing import Any


def streamable_http_client(*args: Any, **kwargs: Any) -> Any:
    class _C:
        async def __aenter__(self) -> Any:
            return self

        async def __aexit__(self, *args: Any) -> None:
            return None
    return _C()
