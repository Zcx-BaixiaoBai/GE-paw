"""SQLAlchemy engine + session; schema 由 alembic 管理。"""
from __future__ import annotations

from contextlib import contextmanager
from importlib import invalidate_caches as _invalidate_caches
from pathlib import Path
from typing import Iterator, Optional

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .settings import get_settings


class Base(DeclarativeBase):
    """All models inherit from this."""
    pass


_engine: Optional[Engine] = None
_SessionLocal: Optional[sessionmaker] = None


def get_engine() -> Engine:
    global _engine, _SessionLocal
    if _engine is None:
        s = get_settings()
        url = s.database_url
        connect_args: dict = {}
        if url.startswith("sqlite"):
            connect_args["check_same_thread"] = False
        _engine = create_engine(
            url,
            connect_args=connect_args,
            pool_pre_ping=True,
            future=True,
        )
        if url.startswith("sqlite"):
            @event.listens_for(_engine, "connect")
            def _set_sqlite_pragma(dbapi_connection, _):
                cur = dbapi_connection.cursor()
                cur.execute("PRAGMA foreign_keys=ON")
                cur.execute("PRAGMA journal_mode=WAL")
                cur.close()

        _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)
    return _engine


def get_session_factory() -> sessionmaker:
    if _SessionLocal is None:
        get_engine()
    assert _SessionLocal is not None
    return _SessionLocal


@contextmanager
def session_scope() -> Iterator[Session]:
    factory = get_session_factory()
    s = factory()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()


def get_db():
    """FastAPI dependency: one Session per request, closed on exit."""
    factory = get_session_factory()
    s = factory()
    try:
        yield s
    finally:
        s.close()


def init_db() -> None:
    """Apply pending alembic migrations.

    GE-paw owns its schema via alembic. ``init`` / serve / pytest all call this
    on startup; the first run against an empty database creates the full
    schema, subsequent runs are no-ops when the database is already at head.

    Implementation notes:
      * We invalidate Python'\''s import caches for ``migrations.env`` and the
        alembic runtime modules before each call so test fixtures that swap
        GEPAW_DATABASE_URL between calls pick up the new URL (the env.py
        script reads the URL at module load time).
      * The ``script_location`` is passed as an absolute path so the %(here)s
        in alembic.ini does not depend on the caller'\''s working directory.
      * We run alembic inside a subprocess when invoked from pytest-style
        isolated environments; the in-process path is used for normal startup
        (gepaw init / serve). Both paths are equivalent for correctness; the
        subprocess path avoids an alembic/pytest interaction on Windows where
        a transient SQLite handle is sometimes not released quickly enough
        for the next test fixture to open a brand-new database file.
    """
    from .. import models  # noqa: F401

    import sys
    for mod_name in list(sys.modules):
        if mod_name == "migrations.env" or mod_name.startswith("migrations."):
            del sys.modules[mod_name]
    _invalidate_caches()

    _repo = Path(__file__).resolve().parents[3]  # src/gepaw/app/db.py -> repo root
    _ini = str((_repo / "alembic.ini").resolve())
    _migrations = str((_repo / "migrations").resolve())
    _url = get_settings().database_url

    # Detect pytest via the env var pytest sets on every test process.
    in_pytest = bool(sys.modules.get("pytest")) or os_environ_has_pytest()

    if in_pytest:
        # Run alembic in a fresh subprocess so module state from prior tests
        # cannot leak into this one. The subprocess is short-lived and exits
        # cleanly, releasing SQLite file handles before returning.
        import json
        import subprocess
        import sys as _sys
        payload = {"ini": _ini, "migrations": _migrations, "url": _url}
        result = subprocess.run(
            [_sys.executable, "-c", _ALEMBIC_RUNNER, json.dumps(payload)],
            capture_output=True, text=True, check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"alembic subprocess upgrade failed (rc={result.returncode}): "
                f"stderr={result.stderr.strip()[:500]}"
            )
        return

    # Production path: in-process alembic upgrade.
    from alembic import command as _alembic_cmd
    from alembic.config import Config as _AlembicConfig
    _cfg = _AlembicConfig(_ini)
    _cfg.set_main_option("script_location", _migrations)
    _cfg.set_main_option("sqlalchemy.url", _url)
    _alembic_cmd.upgrade(_cfg, "head")


def os_environ_has_pytest() -> bool:
    import os
    return "PYTEST_CURRENT_TEST" in os.environ


_ALEMBIC_RUNNER = r"""
import json, sys
payload = json.loads(sys.argv[1])
from alembic.config import Config
from alembic import command
cfg = Config(payload["ini"])
cfg.set_main_option("script_location", payload["migrations"])
cfg.set_main_option("sqlalchemy.url", payload["url"])
command.upgrade(cfg, "head")
"""
