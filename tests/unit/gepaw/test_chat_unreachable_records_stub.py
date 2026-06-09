"""Unit test: /api/client/chat records a stub TokenUsageLog row even when the
configured LLM endpoint is unreachable. The chat route must not silently lose
the usage record on transport failure (this is the same contract channel_manager
already enforces).
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import uuid


def _isolated_env() -> str:
    tmp = tempfile.mkdtemp(prefix="gepaw-chat-fail-")
    os.environ["GEPAW_SECRET_KEY"] = "test-secret-key-32-bytes-padding-padding-pad"
    os.environ["GEPAW_DATA_DIR"] = tmp
    os.environ["GEPAW_DATABASE_URL"] = f"sqlite:///{tmp}/test.db"
    os.environ["GEPAW_DOCS"] = "0"
    for mod in [m for m in list(sys.modules) if m.startswith("gepaw")]:
        del sys.modules[mod]
    return tmp


def test_chat_records_usage_on_unreachable_llm():
    tmp = _isolated_env()
    from fastapi.testclient import TestClient
    from gepaw.app.db import init_db, session_scope
    from gepaw.app._app import app
    from gepaw.app.settings import get_settings
    from gepaw.models.identity import Org, User, Membership
    from gepaw.models.llm import LLMEndpoint
    from gepaw.security.crypto import encrypt
    from gepaw.security.passwords import hash_password

    init_db()
    with session_scope() as db:
        o = Org(name="FailOrg", slug="fail-" + uuid.uuid4().hex[:6])
        db.add(o); db.flush()
        u = User(username="eve", password_hash=hash_password("evepass1234"))
        db.add(u); db.flush()
        db.add(Membership(user_id=u.id, org_id=o.id, role="admin"))
        # Add an LLM endpoint pointing at an unreachable port (so the call fails fast)
        db.add(LLMEndpoint(
            org_id=o.id, name="stub-fail", base_url="http://127.0.0.1:1/v1",
            api_key_enc=encrypt("sk-fail"),
            model="gpt-4o-mini", max_tokens=16, temperature=0.0,
            is_default=True, enabled=True,
        ))
        org_id = o.id

    with TestClient(app) as c:
        r = c.post("/api/auth/login", json={"username": "eve", "password": "evepass1234"})
        assert r.status_code == 200, r.text
        tok = r.json()["access_token"]
        H = {"Authorization": "Bearer " + tok}

        # /api/client/chat -> 200 with "(assistant unavailable: ...)"
        r = c.post("/api/client/chat", json={"message": "hello"}, headers=H)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["tokens_in"] == 0
        assert body["tokens_out"] == 0
        assert "assistant unavailable" in body["reply"]

        # Verify that exactly one TokenUsageLog row was recorded with model="(unreachable)"
        from gepaw.models import TokenUsageLog
        with session_scope() as db:
            rows = db.query(TokenUsageLog).filter(TokenUsageLog.org_id == org_id).all()
            assert len(rows) == 1
            assert rows[0].model == "(unreachable)"
            assert rows[0].prompt_tokens == 0
            assert rows[0].completion_tokens == 0

    shutil.rmtree(tmp, ignore_errors=True)
