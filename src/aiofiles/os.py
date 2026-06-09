"""Stub: aiofiles.os - async wrappers around os functions used by gepaw."""
from __future__ import annotations

import os as _os
import os.path as _ospath


async def stat(file_path, *args, **kwargs):
    return _os.stat(file_path, *args, **kwargs)


async def remove(file_path, *args, **kwargs):
    return _os.remove(file_path, *args, **kwargs)


async def rename(src, dst, *args, **kwargs):
    return _os.rename(src, dst, *args, **kwargs)


async def makedirs(path, *args, **kwargs):
    return _os.makedirs(path, *args, **kwargs)


async def path_exists(path):
    return _ospath.exists(path)