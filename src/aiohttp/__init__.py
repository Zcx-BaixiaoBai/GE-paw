"""Stub: aiohttp for gepaw test isolation."""
from __future__ import annotations

import json as _json
from typing import Any


class ClientSession:
    """Stub aiohttp.ClientSession with context-manager support."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._kwargs = kwargs

    async def __aenter__(self) -> "ClientSession":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def close(self) -> None:
        return None

    def get(self, *args: Any, **kwargs: Any):
        return _RequestContext("GET")

    def post(self, *args: Any, **kwargs: Any):
        return _RequestContext("POST")

    def put(self, *args: Any, **kwargs: Any):
        return _RequestContext("PUT")

    def delete(self, *args: Any, **kwargs: Any):
        return _RequestContext("DELETE")

    def patch(self, *args: Any, **kwargs: Any):
        return _RequestContext("PATCH")


class _RequestContext:
    """Async context manager that yields a fake Response."""

    def __init__(self, method: str) -> None:
        self.method = method

    async def __aenter__(self) -> "Response":
        return Response()

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None


class Response:
    """Stub aiohttp Response."""

    def __init__(self) -> None:
        self.status = 200
        self._data: Any = {}

    async def text(self) -> str:
        return _json.dumps(self._data)

    async def json(self) -> Any:
        return self._data

    async def read(self) -> bytes:
        return b""

    async def __aenter__(self) -> "Response":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None


class ClientError(Exception):
    """Stub aiohttp ClientError."""


class ClientResponseError(ClientError):
    """Stub aiohttp ClientResponseError."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.status = kwargs.get("status", 0)


class ClientTimeout:
    """Stub aiohttp ClientTimeout."""

    def __init__(self, total: float = 0) -> None:
        self.total = total


class WSMsgType:
    """Stub aiohttp WSMsgType constants."""

    TEXT = 1
    BINARY = 2
    CLOSE = 8
    ERROR = 258


def __getattr__(name: str) -> Any:
    """Lazy fallback for additional aiohttp symbols."""

    class _Fallback:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            for k, v in kwargs.items():
                setattr(self, k, v)

    return _Fallback

class FormData:
    """Minimal stub for `aiohttp.FormData`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._fields: list[tuple[str, Any, dict[str, Any]]] = []

    def add_field(
        self,
        name: str,
        data: Any,
        filename: str | None = None,
        content_type: str | None = None,
        **kwargs: Any,
    ) -> None:
        meta = {"filename": filename, "content_type": content_type}
        meta.update(kwargs)
        self._fields.append((name, data, meta))
