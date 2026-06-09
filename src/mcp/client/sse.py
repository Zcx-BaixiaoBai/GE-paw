"""Stub for mcp.client.sse."""
from __future__ import annotations
from typing import Any


class sse_client:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    async def __aenter__(self) -> Any:
        return self

    async def __aexit__(self, *args: Any) -> None:
        return None
