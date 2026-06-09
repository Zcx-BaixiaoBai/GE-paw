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
LLM_RATE_LIMIT_PAUSE = 5.0
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
# ---------------------------------------------------------------------------
# Media directory (channels)
# ---------------------------------------------------------------------------

DEFAULT_MEDIA_DIR = (DATA_DIR / "media").resolve()
DEFAULT_MEDIA_DIR.mkdir(parents=True, exist_ok=True)
# Built-in QA agent skill names (mirrors qwenpaw defaults)
BUILTIN_QA_AGENT_SKILL_NAMES = (
    "ask_user_question",
    "background_task",
    "convert_schemas",
    "create_file",
    "create_plan",
    "edit_file",
    "enter_plan_mode",
    "file_search",
    "get_current_datetime",
    "glob_files",
    "grep_files",
    "list_files",
    "multi_edit_file",
    "notebook_edit",
    "read_file",
    "schedule_task",
    "search_code",
    "share_memory",
    "skill_manage",
    "task_done",
    "task_kill",
    "task_output",
    "task_status",
    "view_image",
    "view_media",
    "view_video",
    "web_extraction",
    "web_search",
    "write_file",
)

# Memory directory (mirrors qwenpaw defaults)
from pathlib import Path as _Path
MEMORY_DIR = (WORKING_DIR / "memory") if isinstance(WORKING_DIR, _Path) else _Path.home() / ".gepaw" / "memory"


# ---------------- additional channels/CLI/runtime constants ----------------
BUILTIN_QA_AGENT_ID = 'qa-bot'
BUILTIN_QA_AGENT_NAME = 'Q&A Bot'
LEGACY_QA_AGENT_ID = 'qa_bot'

CODING_PROJECT_SUBDIR = 'coding_projects'

CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']

CUSTOM_CHANNELS_DIR = WORKING_DIR / 'custom_channels'

DEBUG_HISTORY_FILE = WORKING_DIR / 'debug_history.jsonl'

DEFAULT_LOCAL_PROVIDER_DIR = WORKING_DIR / 'local_models'

HEARTBEAT_TARGET_INBOX = 'inbox'
HEARTBEAT_TARGET_LAST = 'last'

MAX_LOAD_HISTORY_COUNT = 100

MEMORY_COMPACT_KEEP_RECENT = 20
MEMORY_COMPACT_RATIO = 0.5

MODELS_DIR = WORKING_DIR / 'models'

MODEL_PROVIDER_CHECK_TIMEOUT = 5.0

PLUGINS_DIR = WORKING_DIR / 'plugins'

TOKEN_USAGE_FILE = WORKING_DIR / 'token_usage.jsonl'


# Upload media max size in MB
UPLOAD_MAX_SIZE_MB = 50

# Tool guard approval timeout
TOOL_GUARD_APPROVAL_TIMEOUT_SECONDS = 60
