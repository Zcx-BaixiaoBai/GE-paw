"""对称加密（Fernet），用于敏感字段（API Key、频道凭据）。"""
from __future__ import annotations

import base64
import hashlib
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken

from ..app.settings import get_settings


def _key() -> bytes:
    s = get_settings()
    raw = (s.secret_key or "").encode("utf-8")
    if not raw:
        raise RuntimeError("GEPAW_SECRET_KEY 未配置")
    digest = hashlib.sha256(raw).digest()
    return base64.urlsafe_b64encode(digest)


def _fernet() -> Fernet:
    return Fernet(_key())


def encrypt(plaintext: str) -> str:
    if plaintext is None:
        return ""
    return _fernet().encrypt(plaintext.encode("utf-8")).decode("ascii")


def decrypt(token: str) -> Optional[str]:
    if not token:
        return None
    try:
        return _fernet().decrypt(token.encode("ascii")).decode("utf-8")
    except InvalidToken:
        return None
