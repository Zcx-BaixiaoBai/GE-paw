"""Plugin architecture data classes.

Lightweight stand-ins for the dataclass-shaped objects the loader,
API, and tests share. We intentionally avoid pydantic here so the
test surface stays dependency-free; only the fields actually used by
the gepaw plugin subsystem are declared.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class PluginEntryPoints:
    """Plugin entry points for frontend and backend."""

    frontend: Optional[str] = None
    backend: Optional[str] = None


@dataclass
class PluginManifest:
    """Plugin manifest definition (subset we actually use)."""

    id: str
    name: str = ""
    version: str = "0.0.0"
    entry: Optional[PluginEntryPoints] = None
    description: str = ""
    author: str = ""
    plugin_type: str = "general"
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PluginRecord:
    """A loaded plugin record kept by the loader."""

    manifest: PluginManifest
    source_path: Path
    enabled: bool = True
    instance: Optional[Any] = None
    diagnostics: List[str] = field(default_factory=list)