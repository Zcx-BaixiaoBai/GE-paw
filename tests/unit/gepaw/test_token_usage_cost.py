"""Unit tests for token usage tracking and cost table."""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path


def _isolated_env():
    tmp = tempfile.mkdtemp(prefix="gepaw-tok-")
    os.environ["GEPAW_SECRET_KEY"] = "test-secret-key-32-bytes-padding-padding-pad"
    os.environ["GEPAW_DATA_DIR"] = tmp
    os.environ["GEPAW_DATABASE_URL"] = f"sqlite:///{tmp}/test.db"
    os.environ["GEPAW_DOCS"] = "0"
    # Make the package pick up the new env vars
    for mod in [m for m in list(sys.modules) if m.startswith("gepaw")]:
        del sys.modules[mod]
    return tmp


def test_cost_table_known_models():
    _isolated_env()
    from gepaw.token_usage.cost_table import (
        clear_override,
        compute_cost_cents,
        known_models,
        quote_for,
        set_override,
    )
    models = known_models()
    assert "gpt-4o" in models
    assert "gpt-4o-mini" in models
    # known gpt-4o quote -> 250 / 1000 cents per 1K
    q = quote_for("gpt-4o")
    assert q["prompt"] == 250
    assert q["completion"] == 1000
    # 1k prompt + 1k completion should be 250 + 1000 = 1250 cents
    c = compute_cost_cents("gpt-4o", 1000, 1000)
    assert c == 1250
    # unknown model returns 0 cost
    c2 = compute_cost_cents("totally-unknown-model-xyz", 100, 100)
    assert c2 == 0
    # override beats default
    set_override("gpt-4o", 1, 2)
    assert compute_cost_cents("gpt-4o", 1000, 1000) == 1 + 2
    clear_override("gpt-4o")
    assert compute_cost_cents("gpt-4o", 1000, 1000) == 1250


def test_record_usage_inserts_row():
    tmp = _isolated_env()
    from sqlalchemy.orm import Session

    from gepaw.app.db import get_session_factory, init_db, session_scope
    from gepaw.models import Org, User, Membership
    from gepaw.token_usage import record_usage
    from gepaw.token_usage import manager as mgr

    init_db()
    factory = get_session_factory()
    with session_scope() as db:
        o = Org(name="TokOrg", slug="tokorg")
        db.add(o); db.flush()
        u = User(username="alice", password_hash="x")
        db.add(u); db.flush()
        db.add(Membership(user_id=u.id, org_id=o.id, role="admin"))
        org_id = o.id
        user_id = u.id

    with session_scope() as db:
        rid = record_usage(
            db,
            org_id=org_id,
            model="gpt-4o-mini",
            prompt_tokens=500,
            completion_tokens=200,
            user_id=user_id,
            session_id=None,
        )
        assert rid > 0
        # Add a stub call
        record_usage(
            db,
            org_id=org_id,
            model="stub",
            prompt_tokens=0,
            completion_tokens=0,
            user_id=None,
        )

    with session_scope() as db:
        s = mgr.summarize(db, org_id)
        assert s["prompt_tokens"] == 500
        assert s["completion_tokens"] == 200
        # 500/1000*15 + 200/1000*60 = 7.5 + 12 = 19.5 -> 20 cents
        assert s["cost_cents"] >= 19
        assert s["calls"] == 2
        per_model = {row["model"]: row for row in mgr.by_model(db, org_id)}
        assert per_model["gpt-4o-mini"]["calls"] == 1
        assert per_model["stub"]["calls"] == 1
        per_user = {row["user_id"]: row for row in mgr.by_user(db, org_id)}
        assert per_user[user_id]["calls"] == 1
        buckets = mgr.by_day(db, org_id)
        assert len(buckets) == 1
        assert buckets[0].total_tokens == 700
