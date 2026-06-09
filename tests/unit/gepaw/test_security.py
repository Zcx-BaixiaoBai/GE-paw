"""Unit tests for gepaw.security (Fernet roundtrip, JWT encode/decode)."""
from __future__ import annotations

import time
import pytest

from gepaw.security.crypto import encrypt, decrypt
from gepaw.security.jwt import create_access_token, decode_token, create_refresh_token


def test_fernet_roundtrip():
    plain = "sk-very-secret-api-key-1234"
    enc = encrypt(plain)
    assert enc != plain
    assert decrypt(enc) == plain


def test_fernet_empty_string():
    assert decrypt(encrypt("")) == ""


def test_jwt_access_encode_decode():
    token = create_access_token(user_id="u1", org_ids=["o1"], roles_by_org={"o1": "admin"})
    payload = decode_token(token, expected_type="access")
    assert payload["sub"] == "u1"
    assert payload["org_ids"] == ["o1"]
    assert payload["roles"] == {"o1": "admin"}
    assert payload["typ"] == "access"
    assert payload["exp"] > time.time()


def test_jwt_refresh_longer_ttl_than_access():
    a = create_access_token(user_id="u", org_ids=["o"], roles_by_org={"o": "user"}, ttl=60)
    rt, jti = create_refresh_token(user_id="u", ttl=3600)
    pa = decode_token(a, expected_type="access")
    pr = decode_token(rt, expected_type="refresh")
    # refresh should outlive access by at least 30 min in this scenario
    assert pr["exp"] - pa["exp"] >= 1800
    assert pr["jti"] == jti


def test_jwt_decode_rejects_tampered():
    tok = create_access_token(user_id="u", org_ids=["o"], roles_by_org={"o": "admin"})
    tampered = tok[:-2] + ("AA" if tok[-2:] != "AA" else "BB")
    with pytest.raises(Exception):
        decode_token(tampered)
