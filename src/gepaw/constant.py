# -*- coding: utf-8 -*-
"""GE-paw runtime constants."""

import os
from pathlib import Path


class EnvVarLoader:
    """Lightweight helper for reading environment variables.

    gepaw's various subsystems consult configuration through this
    loader so tests can patch ``gepaw.constant.EnvVarLoader.get_str``
    in one place.  Implementation-wise it is a thin wrapper around
    :func:`os.environ.get` with a default of empty string (instead of
    ``None``) and an optional fallback.
    """

    @staticmethod
    def get_str(name: str, default: str = "") -> str:
        return os.environ.get(name, default)

    @staticmethod
    def get_int(name: str, default: int = 0) -> int:
        try:
            return int(os.environ.get(name, default))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def get_bool(name: str, default: bool = False) -> bool:
        raw = os.environ.get(name)
        if raw is None:
            return default
        return raw.strip().lower() in ("1", "true", "yes", "y", "on")


def _resolve_working_dir() -> Path:
    """Pick the gepaw working directory.

    Priority:
    1. ``GEPAW_WORKING_DIR`` env var (if set)
    2. ``~/.gepaw`` (the canonical home for gepaw state)
    """
    explicit = os.environ.get("GEPAW_WORKING_DIR")
    if explicit:
        return Path(explicit).expanduser().resolve()
    return Path("~/.gepaw").expanduser().resolve()


WORKING_DIR = _resolve_working_dir()
WORKING_DIR.mkdir(parents=True, exist_ok=True)


SECRET_DIR = (
    Path(
        EnvVarLoader.get_str(
            "GEPAW_SECRET_DIR",
            str(WORKING_DIR / ".secret"),
        ),
    )
    .expanduser()
)


PROJECT_NAME = "GE-paw"
LOG_LEVEL_ENV = "GEPAW_LOG_LEVEL"
CORS_ORIGINS_ENV = "GEPAW_CORS_ORIGINS"
DOCS_ENABLED = os.environ.get("GEPAW_DOCS", "0") == "1"

DATA_DIR = Path(os.environ.get("GEPAW_DATA_DIR", "./data")).resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = os.environ.get(
    "GEPAW_DATABASE_URL",
    f"sqlite:///{(DATA_DIR / 'gepaw.db').as_posix()}",
)

WIKI_ROOT = (DATA_DIR / "orgs").resolve()
WIKI_ROOT.mkdir(parents=True, exist_ok=True)

UPLOAD_CACHE_DIR = (DATA_DIR / "uploads").resolve()
UPLOAD_CACHE_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE_PATH = DATA_DIR / "gepaw.log"

SECRET_KEY_ENV = "GEPAW_SECRET_KEY"
JWT_ALG = "HS256"
ACCESS_TOKEN_TTL_SECONDS = int(os.environ.get("GEPAW_ACCESS_TTL", str(15 * 60)))
REFRESH_TOKEN_TTL_SECONDS = int(os.environ.get("GEPAW_REFRESH_TTL", str(7 * 24 * 3600)))

LLM_REQUEST_TIMEOUT = int(os.environ.get("GEPAW_LLM_TIMEOUT", "120"))

WIKI_FILE_MAX_BYTES = int(os.environ.get("GEPAW_WIKI_MAX_BYTES", str(1 * 1024 * 1024)))
WIKI_PREVIEW_MAX_BYTES = int(os.environ.get("GEPAW_WIKI_PREVIEW_MAX_BYTES", str(2 * 1024 * 1024)))

DEFAULT_ADMIN_USERNAME = os.environ.get("GEPAW_ADMIN_USERNAME", "admin")
DEFAULT_ADMIN_PASSWORD = os.environ.get("GEPAW_ADMIN_PASSWORD", "")
DEFAULT_ORG_NAME = os.environ.get("GEPAW_ORG_NAME", "Default")

CROSS_CHANNEL_MERGE_DEFAULT = False
CRON_FAILURE_DISABLE_THRESHOLD = 3
SUPPORTED_AGENT_LANGUAGES = ("en", "zh")


# ---------------------------------------------------------------------------
# Marker injection / placeholder used by message normalisation
# ---------------------------------------------------------------------------

TRUNCATION_NOTICE_MARKER = "<<<TRUNCATED>>>"

MEDIA_UNSUPPORTED_PLACEHOLDER = (
    "[Media content removed - model does not support this media type]"
)


# ---------------------------------------------------------------------------
# Heartbeat defaults
# ---------------------------------------------------------------------------

HEARTBEAT_DEFAULT_EVERY = 1800
HEARTBEAT_DEFAULT_TARGET = 8


# ---------------------------------------------------------------------------
# LLM rate limiting / retry defaults
# ---------------------------------------------------------------------------

LLM_MAX_CONCURRENT = 8
LLM_MAX_QPM = 60
LLM_ACQUIRE_TIMEOUT = 30
LLM_MAX_RETRIES = 5
LLM_BACKOFF_BASE = 1.0
LLM_BACKOFF_CAP = 30.0
LLM_RATE_LIMIT_PAUSE = 0.0
LLM_RATE_LIMIT_JITTER = 0.2


# ---------------------------------------------------------------------------
# Multi-agent support
# ---------------------------------------------------------------------------

# gepaw keeps the same QwenPaw flag as a no-op so downstream code can
# safely import it; behaviour is always enabled in gepaw for now.
MULTI_AGENT_ENABLED = True


# ---------------------------------------------------------------------------
# File-based persistence helpers
# ---------------------------------------------------------------------------

JOBS_FILE = EnvVarLoader.get_str("GEPAW_JOBS_FILE", "jobs.json")
CHATS_FILE = EnvVarLoader.get_str("GEPAW_CHATS_FILE", "chats.json")
HEARTBEAT_FILE = EnvVarLoader.get_str("GEPAW_HEARTBEAT_FILE", "HEARTBEAT.md")
PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH_ENV = "PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH"


def _running_in_container() -> bool:
    """Best-effort detection of whether gepaw is running inside a container."""
    import os as _os

    if _os.path.exists("/.dockerenv"):
        return True
    if _os.environ.get("GEPAW_RUNNING_IN_CONTAINER", "").lower() in (
        "1",
        "true",
        "yes",
    ):
        return True
    return False


RUNNING_IN_CONTAINER = _running_in_container()


# ---------------------------------------------------------------------------
# Backup storage location
# ---------------------------------------------------------------------------

BACKUP_DIR = (DATA_DIR / "backups").resolve()
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Config / secret files
# ---------------------------------------------------------------------------

CONFIG_FILE = EnvVarLoader.get_str("GEPAW_CONFIG_FILE", "config.json")