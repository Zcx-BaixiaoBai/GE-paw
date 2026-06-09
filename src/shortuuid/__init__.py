"""Stub shortuuid for gepaw test isolation."""
from __future__ import annotations

import uuid as _uuid
import random as _random


# Mirrors real shortuuid's default alphabet (omits I, l, O, 0 to avoid
# visual ambiguity).
_DEFAULT_ALPHABET = (
    "23456789ABCDEFGHJKMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
)


def uuid():
    """Return a short unique id (22 chars)."""
    return random(22)


def uuid4():
    """Return a full 32-char hex UUID."""
    return _uuid.uuid4().hex


def encode(u, alphabet=_DEFAULT_ALPHABET):
    s = ''
    base = len(alphabet)
    while u > 0:
        u, r = divmod(u, base)
        s = alphabet[r] + s
    return s or alphabet[0]


def random(length=22, alphabet=_DEFAULT_ALPHABET):
    return ''.join(_random.choice(alphabet) for _ in range(length))


class ShortUUID:
    def __init__(self, alphabet=_DEFAULT_ALPHABET):
        self._alphabet = alphabet

    def uuid(self):
        return random(22, self._alphabet)

    def random(self, length=22):
        return random(length, self._alphabet)

    def encode(self, u):
        return encode(u, self._alphabet)

    def decode(self, s):
        return int(s, len(self._alphabet))
