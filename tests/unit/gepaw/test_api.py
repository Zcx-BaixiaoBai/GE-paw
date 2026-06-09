"""End-to-end test for the FastAPI app via TestClient (no real LLM)."""
from __future__ import annotations

import os
import shutil
import tempfile
import uuid
import pytest
from fastapi.testclient import TestClient

from gepaw.app.db import init_db, session_scope
from gepaw.app import db as _dbmod
from gepaw.app.settings import get_settings
from gepaw.app._app import app
from gepaw.models.identity import Org, User, Membership
from gepaw.security.passwords import hash_password


def _reset_db_engine():
    # Drop the module-level singleton so the next get_engine() rebuilds
    # against the new GEPAW_DATABASE_URL.
    if _dbmod._engine is not None:
        try:
            _dbmod._engine.dispose(close=True)
        except Exception:
            pass
    _dbmod._engine = None
    _dbmod._SessionLocal = None


@pytest.fixture
def client(monkeypatch):
    from sqlalchemy.orm import close_all_sessions
    close_all_sessions()
    get_settings.cache_clear()
    tmp = tempfile.mkdtemp(prefix="gepaw-api-" + uuid.uuid4().hex[:6] + "-")
    db = os.path.join(tmp, "test.db")
    monkeypatch.setenv("GEPAW_DATABASE_URL", "sqlite:///" + db)
    monkeypatch.setenv("GEPAW_DATA_DIR", tmp)
    monkeypatch.setenv("GEPAW_SECRET_KEY", "test-secret-key-" + uuid.uuid4().hex)
    get_settings.cache_clear()
    _reset_db_engine()
    init_db()
    org_id = "o-" + uuid.uuid4().hex[:8]
    user_id = "u-" + uuid.uuid4().hex[:8]
    mem_id = "m-" + uuid.uuid4().hex[:8]
    with session_scope() as s:
        org = Org(id=org_id, name="Org1", slug="slug-" + uuid.uuid4().hex[:8])
        s.add(org)
        u = User(id=user_id, username="admin", display_name="Admin", password_hash=hash_password("admin123"))
        s.add(u)
        s.add(Membership(id=mem_id, user_id=u.id, org_id=org.id, role="admin"))
    with TestClient(app) as c:
        yield c
    try:
        _reset_db_engine()
        shutil.rmtree(tmp, ignore_errors=True)
    except Exception:
        pass


def _login(client):
    r = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_login_logout(client):
    tok = _login(client)
    r = client.get("/api/auth/me", headers={"Authorization": "Bearer " + tok})
    assert r.status_code == 200
    assert r.json()["username"] == "admin"


def test_admin_llm_crud(client):
    tok = _login(client)
    H = {"Authorization": "Bearer " + tok}
    r = client.post("/api/admin/llm", json={
        "name": "test", "base_url": "https://x/v1", "api_key": "sk-test",
        "model": "gpt-4o-mini", "max_tokens": 256, "temperature": 0.1, "is_default": True,
    }, headers=H)
    assert r.status_code == 201, r.text
    eid = r.json()["id"]
    r = client.get("/api/admin/llm", headers=H)
    assert r.status_code == 200
    assert any(e["id"] == eid for e in r.json())
    r = client.delete("/api/admin/llm/" + eid, headers=H)
    assert r.status_code == 204


def test_wiki_sandbox_blocks_raw(client):
    tok = _login(client)
    H = {"Authorization": "Bearer " + tok}
    r = client.get("/api/client/wiki/tree?path=wiki/raw", headers=H)
    assert r.status_code == 403
    r = client.get("/api/client/wiki/preview?path=wiki/../etc/passwd", headers=H)
    assert r.status_code == 403
    # Clear cookies set by login so the next request is truly unauthenticated.
    client.cookies.clear()
    r = client.get("/api/client/wiki/tree?path=wiki")
    assert r.status_code == 401


def test_wiki_no_store_middleware(client):
    tok = _login(client)
    H = {"Authorization": "Bearer " + tok}
    r = client.get("/api/client/wiki/tree?path=wiki", headers=H)
    assert r.status_code == 200
    assert "no-store" in r.headers.get("cache-control", "")
