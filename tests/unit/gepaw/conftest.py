"""Shared fixtures and helpers for gepaw unit tests."""
from __future__ import annotations

import os
import shutil
import tempfile
import uuid


def _reset_cached_singletons() -> None:
    try:
        settings_mod = __import__("gepaw.app.settings", fromlist=["get_settings"])
        if hasattr(settings_mod, "get_settings"):
            settings_mod.get_settings.cache_clear()
    except Exception:
        pass
    try:
        db_mod = __import__("gepaw.app.db", fromlist=["_engine", "_SessionLocal"])
        engine = getattr(db_mod, "_engine", None)
        if engine is not None:
            try:
                engine.dispose(close=True)
            except Exception:
                pass
        db_mod._engine = None
        db_mod._SessionLocal = None
    except Exception:
        pass
    try:
        from sqlalchemy.orm import close_all_sessions
        close_all_sessions()
    except Exception:
        pass


def _isolated_env(prefix: str = "gepaw") -> str:
    tmp = tempfile.mkdtemp(prefix=prefix + "-" + uuid.uuid4().hex[:6] + "-")
    os.environ["GEPAW_SECRET_KEY"] = "test-secret-key-" + uuid.uuid4().hex
    os.environ["GEPAW_DATA_DIR"] = tmp
    os.environ["GEPAW_DATABASE_URL"] = "sqlite:///" + os.path.join(tmp, "test.db")
    os.environ["GEPAW_DOCS"] = "0"
    os.environ["GEPAW_DISABLE_CHANNEL_STARTUP"] = "1"
    _reset_cached_singletons()
    return tmp


def _cleanup_isolated_env(tmp: str) -> None:
    _reset_cached_singletons()
    shutil.rmtree(tmp, ignore_errors=True)
