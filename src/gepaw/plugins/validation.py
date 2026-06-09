"""Plugin validation: load a plugin module safely with relative-import support.

Plugins live as a directory on disk.  Their backend file is loaded as
a *package* so relative imports (``from .helpers import ...``) work.
We sanitize the plugin id to a legal Python identifier, register the
module in ``sys.modules`` with the correct ``__package__`` and
``__path__`` so sub-modules are resolvable, and always clean up
``sys.modules`` (and the cached ``__loader__``) in ``finally``.
"""
from __future__ import annotations

import importlib
import importlib.util
import logging
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


logger = logging.getLogger(__name__)


_PREFIX = "_plugin_validation_"


def _sanitize_plugin_id(plugin_id: str) -> str:
    """Map a plugin id like ``my-datapaw`` to a Python identifier."""
    return re.sub(r"[^0-9a-zA-Z_]", "_", plugin_id)


def _already_loaded_submodules(module_name: str) -> list:
    """Return the sys.modules keys registered for *module_name* before we touch it."""
    prefix = module_name + "."
    return [k for k in list(sys.modules) if k == module_name or k.startswith(prefix)]


def _load_submodule(
    module_name: str,
    plugin_dir: Path,
    sub_file: Path,
) -> ModuleType:
    """Load a single sub-module of the plugin package."""
    sub_name = sub_file.stem
    full_name = f"{module_name}.{sub_name}"
    spec = importlib.util.spec_from_file_location(
        full_name,
        sub_file,
        submodule_search_locations=[str(plugin_dir)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not build spec for {sub_file}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[full_name] = module
    spec.loader.exec_module(module)
    return module


def _walk_skill_dir(skills_dir: Path) -> "list[Path]":
    """Return backend file paths discovered alongside the main backend file.

    Plugins typically ship helper modules next to ``plugin.py`` so
    relative imports resolve.  We pick every ``*.py`` file at the
    top level of the plugin dir whose name is not the backend file
    itself.
    """
    if not skills_dir.is_dir():
        return []
    return [
        p
        for p in sorted(skills_dir.iterdir())
        if p.is_file() and p.suffix == ".py" and p.stem != "__init__"
    ]


def validate_plugin_module(
    plugin_id: str,
    plugin_dir: Path,
    backend: str = "plugin.py",
) -> ModuleType:
    """Load the plugin backend as a package so relative imports work.

    Args:
        plugin_id: Plugin id, used to namespace the temporary module
            name. Hyphens and other non-identifier characters are
            replaced with underscores.
        plugin_dir: Directory containing the plugin's backend module
            and any helper modules it imports.
        backend: Filename of the backend entry point (default
            ``plugin.py``).

    Returns:
        The loaded module (its attributes, e.g. ``plugin``, are
        already executed).

    Raises:
        FileNotFoundError: If the backend file does not exist.
        ImportError: If the backend (or any sub-module) fails to
            import.
    """
    plugin_dir = Path(plugin_dir)
    backend_path = plugin_dir / backend
    if not backend_path.is_file():
        raise FileNotFoundError(f"plugin backend not found: {backend_path}")

    safe_id = _sanitize_plugin_id(plugin_id)
    module_name = f"{_PREFIX}{safe_id}"

    # Pre-register helper modules so relative imports resolve during
    # exec_module. We deliberately set ``__package__`` and ``__path__``
    # on the parent module so the parent looks like a package to
    # importlib's loader.
    pre_existing = _already_loaded_submodules(module_name)

    spec = importlib.util.spec_from_file_location(
        module_name,
        backend_path,
        submodule_search_locations=[str(plugin_dir)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not build spec for {backend_path}")

    module = importlib.util.module_from_spec(spec)
    module.__package__ = module_name
    module.__path__ = [str(plugin_dir)]
    sys.modules[module_name] = module

    try:
        for helper in _walk_skill_dir(plugin_dir):
            stem = helper.stem
            if helper == backend_path:
                continue
            # Register sub-module only if it isn't already there
            sub_name = f"{module_name}.{stem}"
            if sub_name not in sys.modules:
                sub_spec = importlib.util.spec_from_file_location(
                    sub_name,
                    helper,
                    submodule_search_locations=[str(plugin_dir)],
                )
                if sub_spec is None or sub_spec.loader is None:
                    continue
                sub_module = importlib.util.module_from_spec(sub_spec)
                sys.modules[sub_name] = sub_module
                try:
                    sub_spec.loader.exec_module(sub_module)
                except Exception:
                    # Sub-module import failures bubble up; we still
                    # clean up below before re-raising.
                    raise

        spec.loader.exec_module(module)
        return module
    finally:
        # Always clean up: drop every module we registered for this
        # validation, even on ImportError, so subsequent runs (or
        # retries) start from a clean slate.
        for key in _already_loaded_submodules(module_name):
            sys.modules.pop(key, None)
        # Also clear any submodules we registered that weren't there
        # before (defensive)
        for key in [k for k in list(sys.modules) if k.startswith(module_name + ".")]:
            if key not in pre_existing:
                sys.modules.pop(key, None)
        if module_name in sys.modules and module_name not in pre_existing:
            sys.modules.pop(module_name, None)
        # Drop importlib's loader cache entry so a subsequent
        # validate_plugin_module call rebuilds the spec from scratch.
        importlib.invalidate_caches()