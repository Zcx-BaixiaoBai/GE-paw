"""Unit tests for the client extras router (Diff / Plan / Preview-data)."""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import uuid


def _isolated_env() -> str:
    tmp = tempfile.mkdtemp(prefix="gepaw-extras-")
    os.environ["GEPAW_SECRET_KEY"] = "test-secret-key-32-bytes-padding-padding-pad"
    os.environ["GEPAW_DATA_DIR"] = tmp
    os.environ["GEPAW_DATABASE_URL"] = f"sqlite:///{tmp}/test.db"
    os.environ["GEPAW_DOCS"] = "0"
    for mod in [m for m in list(sys.modules) if m.startswith("gepaw")]:
        del sys.modules[mod]
    return tmp


def test_diff_404_on_missing(tmp_path: str = "") -> None:
    tmp = _isolated_env()
    from fastapi.testclient import TestClient
    from gepaw.app.db import init_db, session_scope
    from gepaw.app._app import app
    from gepaw.models.identity import Org, User, Membership
    from gepaw.security.passwords import hash_password

    init_db()
    with session_scope() as db:
        o = Org(name="ExtrasOrg", slug="extras-org-" + uuid.uuid4().hex[:6])
        db.add(o); db.flush()
        u = User(username="alice", password_hash=hash_password("alicepw123"))
        db.add(u); db.flush()
        db.add(Membership(user_id=u.id, org_id=o.id, role="admin"))
        org_id = o.id
    with TestClient(app) as c:
        r = c.post("/api/auth/login", json={"username": "alice", "password": "alicepw123"})
        assert r.status_code == 200, r.text
        tok = r.json()["access_token"]
        H = {"Authorization": "Bearer " + tok}
        r = c.get("/api/client/diff?left=wiki/x&right=wiki/y", headers=H)
        assert r.status_code == 404
        assert "left not found" in r.text or "right not found" in r.text
        r = c.get("/api/client/preview-data?path=wiki/x", headers=H)
        assert r.status_code == 404
    shutil.rmtree(tmp, ignore_errors=True)


def test_plan_empty_session_returns_empty_steps() -> None:
    tmp = _isolated_env()
    from fastapi.testclient import TestClient
    from gepaw.app.db import init_db, session_scope
    from gepaw.app._app import app
    from gepaw.models.identity import Org, User, Membership
    from gepaw.models.assistant import ChatSession
    from gepaw.security.passwords import hash_password

    init_db()
    with session_scope() as db:
        o = Org(name="PlanOrg", slug="plan-org-" + uuid.uuid4().hex[:6])
        db.add(o); db.flush()
        u = User(username="bob", password_hash=hash_password("bobpass1234"))
        db.add(u); db.flush()
        db.add(Membership(user_id=u.id, org_id=o.id, role="user"))
        db.flush()
        s = ChatSession(org_id=o.id, user_id=u.id, title="empty-plan")
        db.add(s); db.flush()
        sid = s.id
    with TestClient(app) as c:
        r = c.post("/api/auth/login", json={"username": "bob", "password": "bobpass1234"})
        assert r.status_code == 200, r.text
        tok = r.json()["access_token"]
        H = {"Authorization": "Bearer " + tok}
        r = c.get("/api/client/plan?session_id=" + sid, headers=H)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["session_id"] == sid
        assert body["steps"] == []
        assert body["status"] == "empty"
    shutil.rmtree(tmp, ignore_errors=True)


def test_plan_renders_tool_calls_json() -> None:
    tmp = _isolated_env()
    from fastapi.testclient import TestClient
    from gepaw.app.db import init_db, session_scope
    from gepaw.app._app import app
    from gepaw.models.identity import Org, User, Membership
    from gepaw.models.assistant import ChatSession, Message
    from gepaw.security.passwords import hash_password
    import json as _json

    init_db()
    with session_scope() as db:
        o = Org(name="ToolOrg", slug="tool-org-" + uuid.uuid4().hex[:6])
        db.add(o); db.flush()
        u = User(username="carol", password_hash=hash_password("carolpass123"))
        db.add(u); db.flush()
        db.add(Membership(user_id=u.id, org_id=o.id, role="user"))
        db.flush()
        s = ChatSession(org_id=o.id, user_id=u.id, title="with-tools")
        db.add(s); db.flush()
        m = Message(
            session_id=s.id, role="assistant", content="using tool",
            tool_calls_json=_json.dumps([{"name": "search", "arguments": {"q": "hi"}, "status": "ok"}]),
        )
        db.add(m); db.flush()
        sid = s.id
    with TestClient(app) as c:
        r = c.post("/api/auth/login", json={"username": "carol", "password": "carolpass123"})
        assert r.status_code == 200, r.text
        tok = r.json()["access_token"]
        H = {"Authorization": "Bearer " + tok}
        r = c.get("/api/client/plan?session_id=" + sid, headers=H)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["status"] == "ok"
        assert len(body["steps"]) == 1
        step = body["steps"][0]
        assert step["tool"] == "search"
        assert step["args"] == {"q": "hi"}
    shutil.rmtree(tmp, ignore_errors=True)


def test_diff_requires_auth() -> None:
    tmp = _isolated_env()
    from fastapi.testclient import TestClient
    from gepaw.app.db import init_db
    from gepaw.app._app import app

    init_db()
    with TestClient(app) as c:
        r = c.get("/api/client/diff?left=wiki/x&right=wiki/y")
        assert r.status_code == 401
    shutil.rmtree(tmp, ignore_errors=True)
