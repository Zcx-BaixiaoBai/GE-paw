"""Stub for shortuuid library."""
from __future__ import annotations
import uuid
import random
import string


_ALPHABET = string.digits + string.ascii_letters


def uuid() -> str:
    return str(uuid4())


def uuid4() -> str:
    return uuid.uuid4().hex


def encode(u: int, alphabet: str = _ALPHABET) -> str:
    s = ''
    base = len(alphabet)
    while u > 0:
        u, r = divmod(u, base)
        s = alphabet[r] + s
    return s or alphabet[0]


def random(length: int = 22, alphabet: str = _ALPHABET) -> str:
    return ''.join(random.choice(alphabet) for _ in range(length))


class ShortUUID:
    def __init__(self, alphabet: str = _ALPHABET) -> None:
        self._alphabet = alphabet

    def uuid(self) -> str:
        return uuid.uuid4().hex

    def random(self, length: int = 22) -> str:
        return random(length, self._alphabet)

    def encode(self, u: int) -> str:
        return encode(u, self._alphabet)

    def decode(self, s: str) -> int:
        return int(s, len(self._alphabet))
