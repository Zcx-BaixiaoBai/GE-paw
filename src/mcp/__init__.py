"""Stub for mcp package."""
from __future__ import annotations
from typing import Any


class ClientSession:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    async def __aenter__(self) -> "ClientSession":
        return self

    async def __aexit__(self, *args: Any) -> None:
        return None

    async def list_tools(self) -> Any:
        return None

    async def call_tool(self, *args: Any, **kwargs: Any) -> Any:
        return None

    async def initialize(self) -> Any:
        return None


class Tool:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
