"""统一日志配置。"""
from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "warn": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}
_CONFIGURED = False
LOG_FILE_PATH: Optional[Path] = None


def setup_logger(level: str = "info", log_file: Optional[Path] = None) -> logging.Logger:
    global _CONFIGURED, LOG_FILE_PATH
    root = logging.getLogger("gepaw")
    if _CONFIGURED:
        return root
    root.setLevel(_LEVELS.get((level or "info").lower(), logging.INFO))
    root.propagate = False

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(fmt)
    root.addHandler(sh)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8")
        fh.setFormatter(fmt)
        root.addHandler(fh)
        LOG_FILE_PATH = log_file

    _CONFIGURED = True
    return root


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"gepaw.{name}" if not name.startswith("gepaw") else name)
