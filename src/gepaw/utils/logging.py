"""统一日志配置。"""
from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Union

LOG_NAMESPACE = "gepaw"

_LEVEL_MAP: dict = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "warn": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
    "fatal": logging.CRITICAL,
}

LOG_FILE_PATH = None


def _resolve_level(level):
    if isinstance(level, int):
        return level
    if isinstance(level, str):
        return _LEVEL_MAP.get(level.strip().lower(), logging.INFO)
    return logging.INFO


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: chr(27) + "[37m",
        logging.INFO: chr(27) + "[36m",
        logging.WARNING: chr(27) + "[33m",
        logging.ERROR: chr(27) + "[31m",
        logging.CRITICAL: chr(27) + "[1;31m",
    }
    RESET = chr(27) + "[0m"

    def __init__(self, fmt=None, datefmt=None, style="%"):
        if fmt is None:
            fmt = "%(message)s"
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def format(self, record):
        body = super().format(record)
        level_name = logging.getLevelName(record.levelno)
        prefix = "[%s] %s:%d - " % (level_name, record.pathname, record.lineno)
        rendered = prefix + body
        if not sys.stderr.isatty():
            return rendered
        color = self.COLORS.get(record.levelno, "")
        if not color:
            return rendered
        return color + rendered + self.RESET


class SuppressPathAccessLogFilter(logging.Filter):
    def __init__(self, substrings=None):
        super().__init__()
        self.substrings = list(substrings) if substrings else []

    def filter(self, record):
        try:
            msg = record.getMessage()
        except Exception:
            return True
        for needle in self.substrings:
            if needle in msg:
                return False
        return True


def _stream_formatter():
    return logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )


def _has_stream_handler(logger):
    for h in logger.handlers:
        if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler):
            return True
    return False


def add_project_file_handler(path):
    global LOG_FILE_PATH
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(LOG_NAMESPACE)
    target = file_path.resolve()
    for h in logger.handlers:
        if isinstance(h, logging.FileHandler):
            base = getattr(h, "baseFilename", None)
            if base:
                try:
                    if Path(base).resolve() == target:
                        return logger
                except OSError:
                    continue
    fh = RotatingFileHandler(file_path, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8")
    fh.setFormatter(_stream_formatter())
    logger.addHandler(fh)
    LOG_FILE_PATH = file_path
    return logger


def setup_logger(level="info", log_file=None):
    logger = logging.getLogger(LOG_NAMESPACE)
    logger.setLevel(_resolve_level(level))
    logger.propagate = False
    if not _has_stream_handler(logger):
        sh = logging.StreamHandler(sys.stderr)
        sh.setFormatter(_stream_formatter())
        logger.addHandler(sh)
    if log_file is not None:
        add_project_file_handler(log_file)
    return logger


def get_logger(name):
    if name.startswith(LOG_NAMESPACE):
        return logging.getLogger(name)
    return logging.getLogger(LOG_NAMESPACE + "." + name)