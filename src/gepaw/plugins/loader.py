"""Plugin loader: discover, install, and unload plugins.

A minimal, self-contained loader focused on the surfaces exercised
by the current tests:
- ``PluginLoader(plugin_dirs=[])`` + ``.registry`` assignment
- ``_loaded_plugins`` dict of ``plugin_id -> PluginRecord``
- ``unload_plugin(plugin_id, delete_files=False)`` async, which runs
  every uninstall hook (sync or async) in priority order, isolates
  errors, and removes the plugin from the registry on success.

The loader is otherwise a stub; it does not auto-discover or import
plugin modules on its own.  Production code is expected to drive the
loader explicitly.
"""
from __future__ import annotations

import asyncio
import inspect
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .architecture import PluginRecord
from .registry import PluginRegistry


logger = logging.getLogger(__name__)


class PluginLoader:
    """In-memory registry of loaded plugins plus the uninstall lifecycle."""

    def __init__(self, plugin_dirs: Optional[Iterable[Path]] = None) -> None:
        self.plugin_dirs: List[Path] = [Path(p) for p in (plugin_dirs or [])]
        self.registry: PluginRegistry = PluginRegistry()
        self._loaded_plugins: Dict[str, PluginRecord] = {}

    # ------------------------------------------------------------------
    # Inspection helpers
    # ------------------------------------------------------------------

    @property
    def loaded_plugins(self) -> Dict[str, PluginRecord]:
        return dict(self._loaded_plugins)

    def is_loaded(self, plugin_id: str) -> bool:
        return plugin_id in self._loaded_plugins

    def get_record(self, plugin_id: str) -> Optional[PluginRecord]:
        return self._loaded_plugins.get(plugin_id)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def register(self, record: PluginRecord) -> None:
        """Record a plugin as loaded (used by tests to inject state)."""
        self._loaded_plugins[record.manifest.id] = record

    async def unload_plugin(
        self, plugin_id: str, delete_files: bool = False
    ) -> bool:
        """Run uninstall hooks, then drop the plugin from the registry.

        Returns True if a plugin was actually unloaded.  Errors raised
        by individual hooks are logged and swallowed so one bad hook
        cannot prevent cleanup.
        """
        record = self._loaded_plugins.get(plugin_id)
        if record is None:
            logger.debug("unload_plugin: %s not loaded", plugin_id)
            return False

        # Run uninstall hooks in priority order, sync and async both ok.
        for hook in self.registry.get_uninstall_hooks(plugin_id):
            try:
                if inspect.iscoroutinefunction(hook.callback):
                    await hook.callback(plugin_id, delete_files=delete_files)
                else:
                    await asyncio.to_thread(
                        hook.callback, plugin_id, delete_files=delete_files
                    )
            except Exception:  # noqa: BLE001 - hook errors are isolated
                logger.exception(
                    "uninstall hook %s for plugin %s failed",
                    hook.hook_name,
                    plugin_id,
                )

        # Clean up registry registrations owned by this plugin
        self.registry.unregister_plugin(plugin_id)
        self._loaded_plugins.pop(plugin_id, None)
        return True