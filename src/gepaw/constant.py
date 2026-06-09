"""GE-paw 运行时常量。"""
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
WIKI_PREVIEW_MAX_BYTES = int(os.environ.get("GEPAW_WIKI_PREVIEW_PREVIEW", str(2 * 1024 * 1024)))

DEFAULT_ADMIN_USERNAME = os.environ.get("GEPAW_ADMIN_USERNAME", "admin")
DEFAULT_ADMIN_PASSWORD = os.environ.get("GEPAW_ADMIN_PASSWORD", "")
DEFAULT_ORG_NAME = os.environ.get("GEPAW_ORG_NAME", "Default")

CROSS_CHANNEL_MERGE_DEFAULT = False
CRON_FAILURE_DISABLE_THRESHOLD = 3