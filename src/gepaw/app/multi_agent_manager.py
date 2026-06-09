"""Multi-agent manager: coordinates per-agent workspaces and startup hooks.

This module is intentionally minimal — gepaw's full multi-agent
machinery lives in the FastAPI app, but the plugin system needs a
stable home for ``_fire_workspace_created_hooks`` so the host can
broadcast workspace-creation events to plugins.  A static method on
:class:`MultiAgentManager` is the simplest place to put that.

Adding more agent-management code here later is fine; the
:class:`MultiAgentManager` class is meant to grow into the real
multi-agent coordinator.
"""
from __future__ import annotations

import asyncio
import inspect
import logging
from typing import Any, Dict


logger = logging.getLogger(__name__)


class MultiAgentManager:
    """Coordinator for per-agent workspaces and plugin hook dispatch."""

    @staticmethod
    async def _fire_workspace_created_hooks(workspace_info: Dict[str, Any]) -> None:
        """Invoke every registered ``workspace_created`` hook.

        Sync callbacks are offloaded to a worker thread via
        :func:`asyncio.to_thread` so they never block the event loop.
        Async callbacks are awaited directly.  Errors in any single
        hook are logged and swallowed so they cannot prevent
        subsequent hooks from running.
        """
        try:
            from gepaw.plugins.registry import PluginRegistry

            hooks = PluginRegistry().get_workspace_created_hooks()
        except Exception:  # noqa: BLE001 - plugin system not initialised yet
            return

        for hook in hooks:
            try:
                if inspect.iscoroutinefunction(hook.callback):
                    await hook.callback(workspace_info)
                else:
                    await asyncio.to_thread(hook.callback, workspace_info)
            except Exception:  # noqa: BLE001 - hook errors are non-fatal
                logger.error(
                    "workspace_created hook %s for plugin %s raised",
                    hook.hook_name,
                    hook.plugin_id,
                    exc_info=True,
                )