"""JWT 签发与校验。"""
from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

import jwt

from ..app.settings import get_settings
from ..exceptions import AuthError


def create_access_token(*, user_id: str, org_ids: List[str], roles_by_org: Dict[str, str], ttl: Optional[int] = None) -> str:
    s = get_settings()
    now = int(time.time())
    payload = {
        "sub": str(user_id),
        "org_ids": list(org_ids),
        "roles": roles_by_org,
        "iat": now,
        "exp": now + (ttl or s.access_ttl),
        "jti": uuid.uuid4().hex,
        "typ": "access",
    }
    return jwt.encode(payload, s.secret_key, algorithm=s.jwt_alg)


def create_refresh_token(*, user_id: str, ttl: Optional[int] = None) -> Tuple[str, str]:
    s = get_settings()
    jti = uuid.uuid4().hex
    now = int(time.time())
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + (ttl or s.refresh_ttl),
        "jti": jti,
        "typ": "refresh",
    }
    token = jwt.encode(payload, s.secret_key, algorithm=s.jwt_alg)
    return token, jti


def decode_token(token: str, *, expected_type: Optional[str] = None) -> Dict[str, Any]:
    s = get_settings()
    try:
        payload = jwt.decode(token, s.secret_key, algorithms=[s.jwt_alg])
    except jwt.ExpiredSignatureError as e:
        raise AuthError("token 已过期", code="token_expired") from e
    except jwt.InvalidTokenError as e:
        raise AuthError("token 无效", code="token_invalid") from e
    if expected_type is not None and payload.get("typ") != expected_type:
        raise AuthError("token 类型错误", code="token_type_mismatch")
    return payload
