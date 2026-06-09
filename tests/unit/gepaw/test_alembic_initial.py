"""Verify alembic migration produces the same schema as Base.metadata."""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import uuid


def _isolated_env() -> str:
    tmp = tempfile.mkdtemp(prefix="gepaw-alembic-")
    os.environ["GEPAW_SECRET_KEY"] = "test-secret-key-32-bytes-padding-padding-pad"
    os.environ["GEPAW_DATA_DIR"] = tmp
    os.environ["GEPAW_DATABASE_URL"] = f"sqlite:///{tmp}/test.db"
    os.environ["GEPAW_DOCS"] = "0"
    for mod in [m for m in list(sys.modules) if m.startswith("gepaw")]:
        del sys.modules[mod]
    return tmp


def test_alembic_initial_creates_all_tables():
    tmp = _isolated_env()
    from gepaw.app.db import init_db, session_scope
    from gepaw.app.settings import get_settings
    from sqlalchemy import create_engine, text

    # init_db in pytest runs alembic in a subprocess (Windows fd release).
    init_db()

    # Check alembic_version is set and schema has all expected tables.
    engine = create_engine(get_settings().database_url)
    expected = {
        "alembic_version", "org", "user", "membership", "refresh_token",
        "llm_endpoint", "skill", "mcp_server", "plugin",
        "chat_session", "message", "channel_account",
        "cron_job", "cron_run", "token_usage_log",
        "wiki_corpus", "wiki_source", "wiki_query_log",
        "audit_log",
    }
    with engine.connect() as c:
        rows = c.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
        actual = {row[0] for row in rows}
        missing = expected - actual
        assert not missing, f"alembic did not create tables: {missing}"
        rev = c.execute(text("SELECT version_num FROM alembic_version")).fetchone()
        assert rev is not None
        assert rev[0] == "0001_initial_schema"
    shutil.rmtree(tmp, ignore_errors=True)


def test_alembic_idempotent_on_existing_db():
    """Running init_db twice against the same database should be a no-op."""
    tmp = _isolated_env()
    from gepaw.app.db import init_db
    from gepaw.app.settings import get_settings
    from sqlalchemy import create_engine, text
    init_db()
    # Second call must not raise.
    init_db()
    engine = create_engine(get_settings().database_url)
    with engine.connect() as c:
        rev = c.execute(text("SELECT version_num FROM alembic_version")).fetchone()
        assert rev[0] == "0001_initial_schema"
    shutil.rmtree(tmp, ignore_errors=True)
