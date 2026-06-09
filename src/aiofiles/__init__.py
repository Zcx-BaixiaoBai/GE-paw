"""Minimal stub for aiofiles used by gepaw tests."""
from __future__ import annotations

import builtins as _builtins


class _AsyncFile:
    """File object that exposes an async-compatible surface.

    Used with ``async with aiofiles.open(...) as f:`` syntax.
    """

    def __init__(self, fp):
        self._fp = fp

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self._fp.close()
        return False

    async def read(self, *args, **kwargs):
        return self._fp.read(*args, **kwargs)

    async def readline(self, *args, **kwargs):
        return self._fp.readline(*args, **kwargs)

    async def readlines(self, *args, **kwargs):
        return self._fp.readlines(*args, **kwargs)

    async def write(self, *args, **kwargs):
        return self._fp.write(*args, **kwargs)

    async def flush(self):
        return self._fp.flush()

    def close(self):
        self._fp.close()

    def __aiter__(self):
        return self

    async def __anext__(self):
        line = self._fp.readline()
        if not line:
            raise StopAsyncIteration
        return line


def open(file, mode="r", *args, **kwargs):
    """Open a file asynchronously.

    Returns an :class:`_AsyncFile` directly (NOT awaitable) so it can
    be used with ``async with aiofiles.open(...) as f:`` syntax.
    """
    f = _builtins.open(file, mode, *args, **kwargs)
    return _AsyncFile(f)