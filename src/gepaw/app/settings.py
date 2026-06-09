"""GE-paw 全局设置：从环境变量与 .env 文件加载。"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="GEPAW_",
        env_file=os.environ.get("GEPAW_ENV_FILE", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    project_name: str = "GE-paw"
    debug: bool = False
    log_level: str = "info"

    data_dir: Path = Path("./data")
    database_url: str = "sqlite:///./data/gepaw.db"

    secret_key: str = "change-me-in-production-please-this-is-not-secure"
    jwt_alg: str = "HS256"
    access_ttl: int = 15 * 60
    refresh_ttl: int = 7 * 24 * 3600

    host: str = "0.0.0.0"
    port: int = 8765
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"])

    llm_timeout: int = 120

    wiki_max_bytes: int = 1 * 1024 * 1024
    wiki_preview_max_bytes: int = 2 * 1024 * 1024

    admin_username: str = "admin"
    admin_password: Optional[str] = None
    org_name: str = "Default"

    cron_failure_disable_threshold: int = 3
    docs_enabled: bool = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    s = Settings()
    s.data_dir.mkdir(parents=True, exist_ok=True)
    return s
