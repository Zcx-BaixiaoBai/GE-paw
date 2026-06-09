"""Unit tests for WikiNoStoreMiddleware on the new client extras routes."""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import uuid


def _isolated_env() -> str:
    from conftest import _isolated_env as _cf_isolated_env
    return _cf_isolated_env("gepaw-nostore")

def test_extras_routes_have_no_store_header():
    tmp = _isolated_env()
    from fastapi.testclient import TestClient
    from gepaw.app.db import init_db, session_scope
    from gepaw.app._app import app
    from gepaw.models.identity import Org, User, Membership
    from gepaw.security.passwords import hash_password

    init_db()
    with session_scope() as db:
        o = Org(name="NoStoreOrg", slug="nostore-" + uuid.uuid4().hex[:6])
        db.add(o); db.flush()
        u = User(username="dora", password_hash=hash_password("dorapass1234"))
        db.add(u); db.flush()
        db.add(Membership(user_id=u.id, org_id=o.id, role="admin"))

    with TestClient(app) as c:
        r = c.post("/api/auth/login", json={"username": "dora", "password": "dorapass1234"})
        assert r.status_code == 200, r.text
        tok = r.json()["access_token"]
        H = {"Authorization": "Bearer " + tok}

        # /client/diff hits wiki data -> no-store
        r = c.get("/api/client/diff?left=wiki/x&right=wiki/y", headers=H)
        assert r.status_code == 404
        assert "no-store" in r.headers.get("cache-control", "")

        # /client/preview-data -> no-store
        r = c.get("/api/client/preview-data?path=wiki/none.md", headers=H)
        assert r.status_code == 404
        assert "no-store" in r.headers.get("cache-control", "")

        # /client/plan -> no-store (it reads session tool_calls; still wiki-related)
        r = c.get("/api/client/plan?session_id=bogus", headers=H)
        assert r.status_code == 404
        assert "no-store" in r.headers.get("cache-control", "")

    shutil.rmtree(tmp, ignore_errors=True)
