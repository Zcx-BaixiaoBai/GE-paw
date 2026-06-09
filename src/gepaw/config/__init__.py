"""gepaw.config: configuration loading and accessors.

This package provides:
- :func:`load_config` / :func:`save_config` for config.json round-trip
- :class:`Config` and friends for typed access to the config tree
- :mod:`gepaw.config.context` for the workspace context variable

The default loader is intentionally tolerant: when the file is
missing or invalid it logs a warning and returns a sentinel object
whose ``security.tool_guard`` attribute is an empty placeholder so
attribute lookups don't crash. Tests typically patch this function
out and supply a MagicMock.
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict


logger = logging.getLogger(__name__)


_DEFAULT_CONFIG_PATH = Path(
    os.environ.get("GEPAW_CONFIG_PATH", "./data/config.json"),
)


def get_config_path() -> Path:
    """Return the path to the active config.json file."""
    return _DEFAULT_CONFIG_PATH


def load_config(path: Path | None = None) -> Any:
    """Load the gepaw config and return a config object.

    Tests typically patch this function out. The real loader is
    best-effort: a missing or invalid file produces a sentinel
    config with empty tool_guard settings.
    """
    cfg_path = path or get_config_path()
    if not cfg_path.is_file():
        logger.debug("config not found at %s; using defaults", cfg_path)
        return _make_default_config()

    try:
        with cfg_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("failed to load config %s: %s", cfg_path, exc)
        return _make_default_config()
    return _wrap(data)


def save_config(cfg: Any, path: Path | None = None) -> None:
    """Persist *cfg* to disk as JSON (best-effort)."""
    cfg_path = path or get_config_path()
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    if hasattr(cfg, "model_dump"):
        data = cfg.model_dump()
    elif isinstance(cfg, dict):
        data = cfg
    else:
        data = dict(cfg)
    try:
        with cfg_path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
    except OSError as exc:
        logger.warning("failed to save config %s: %s", cfg_path, exc)


# ---------------------------------------------------------------------------
# Sentinel shapes
# ---------------------------------------------------------------------------


class _ToolGuardSentinel:
    """Placeholder that mimics the ``tool_guard`` section."""

    def __init__(self, data: Dict[str, Any] | None = None) -> None:
        data = data or {}
        self.guarded_tools = data.get("guarded_tools")
        self.denied_tools = data.get("denied_tools")
        self.auto_denied_rules = data.get("auto_denied_rules")
        self.enabled = data.get("enabled", True)
        self.rules = data.get("rules", [])


class _SecuritySentinel:
    def __init__(self, data: Dict[str, Any] | None = None) -> None:
        data = data or {}
        self.tool_guard = _ToolGuardSentinel(data.get("tool_guard"))


class _ConfigSentinel:
    """Plain Python object with a ``security`` attribute."""

    def __init__(self, data: Dict[str, Any] | None = None) -> None:
        data = data or {}
        self.security = _SecuritySentinel(data.get("security"))
        self._raw = data

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._raw)


def _make_default_config() -> "_ConfigSentinel":
    return _ConfigSentinel({})


def _wrap(data: Dict[str, Any]) -> "_ConfigSentinel":
    return _ConfigSentinel(data)