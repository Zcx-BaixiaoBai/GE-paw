"""Stub for segno QR code library."""
from __future__ import annotations
from typing import Any


class _QRCode:
    def __init__(self, payload: str = '', **kwargs: Any) -> None:
        self.payload = payload
        for k, v in kwargs.items():
            setattr(self, k, v)

    def save(self, target, **kwargs: Any) -> Any:
        if hasattr(target, 'write'):
            target.write(b'\x89PNG\r\n\x1a\n')
            return None
        with open(target, 'wb') as fh:
            fh.write(b'\x89PNG\r\n\x1a\n')
        return None

    def png_data(self, **kwargs: Any) -> bytes:
        return b'\x89PNG\r\n\x1a\n'

    def svg_data(self, **kwargs: Any) -> bytes:
        return b'<svg/>'


def make(content: str, **kwargs: Any) -> _QRCode:
    return _QRCode(content, **kwargs)
