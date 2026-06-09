"""Stub for nio.crypto.attachments."""
from __future__ import annotations
from typing import Any, Optional


def decrypt_attachment(ciphertext: bytes, key: Any, hash_str: str) -> bytes:
    """Return the ciphertext as-is (stub)."""
    return ciphertext


def encrypt_attachment(plaintext: bytes, key: Any = None) -> tuple[bytes, str, str]:
    """Return (plaintext, '', '') (stub)."""
    return plaintext, '', ''
