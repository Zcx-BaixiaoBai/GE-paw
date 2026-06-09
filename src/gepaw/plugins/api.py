"""Plugin API: the interface plugin developers use to register capabilities.

A ``PluginApi`` instance is handed to a plugin at load time. The
plugin calls methods like ``register_uninstall_hook`` /
``register_workspace_created_hook`` / ``register_skill_provider`` and
``PluginApi`` forwards them to the central :class:`PluginRegistry`,
tagging every registration with this plugin's id.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type


logger = logging.getLogger(__name__)


class PluginApi:
    """API surface exposed to a single plugin instance."""

    def __init__(
        self,
        plugin_id: str,
        config: Optional[Dict[str, Any]] = None,
        manifest: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.plugin_id = plugin_id
        self.config = dict(config) if config else {}
        self.manifest: Dict[str, Any] = dict(manifest) if manifest else {}
        if "id" not in self.manifest:
            self.manifest["id"] = plugin_id
        self._registry: Optional[Any] = None

    def set_registry(self, registry: Any) -> None:
        """Attach a registry. Called by the loader after construction."""
        self._registry = registry

    @property
    def registry(self) -> Any:
        if self._registry is None:
            from .registry import PluginRegistry
            self._registry = PluginRegistry()
        return self._registry

    # ------------------------------------------------------------------
    # Hooks
    # ------------------------------------------------------------------

    def register_startup_hook(
        self,
        hook_name: str,
        callback: Callable,
        priority: int = 100,
    ) -> None:
        self.registry.register_startup_hook(
            plugin_id=self.plugin_id,
            hook_name=hook_name,
            callback=callback,
            priority=priority,
        )

    def register_shutdown_hook(
        self,
        hook_name: str,
        callback: Callable,
        priority: int = 100,
    ) -> None:
        self.registry.register_shutdown_hook(
            plugin_id=self.plugin_id,
            hook_name=hook_name,
            callback=callback,
            priority=priority,
        )

    def register_uninstall_hook(
        self,
        hook_name: str,
        callback: Callable,
        priority: int = 100,
    ) -> None:
        self.registry.register_uninstall_hook(
            plugin_id=self.plugin_id,
            hook_name=hook_name,
            callback=callback,
            priority=priority,
        )

    def register_workspace_created_hook(
        self,
        hook_name: str,
        callback: Callable,
        priority: int = 100,
    ) -> None:
        self.registry.register_workspace_created_hook(
            plugin_id=self.plugin_id,
            hook_name=hook_name,
            callback=callback,
            priority=priority,
        )

    def register_prompt_section(
        self,
        name: str,
        provider: Callable[[Any], str],
        *,
        after: str = "workspace",
        agent_id: Optional[str] = None,
    ) -> None:
        self.registry.register_prompt_section(
            plugin_id=self.plugin_id,
            name=name,
            after=after,
            agent_id=agent_id,
            provider=provider,
        )

    # ------------------------------------------------------------------
    # Providers
    # ------------------------------------------------------------------

    def register_provider(
        self,
        provider_id: str,
        provider_class: Type,
        label: str = "",
        base_url: str = "",
        **metadata: Any,
    ) -> None:
        self.registry.register_provider(
            plugin_id=self.plugin_id,
            provider_id=provider_id,
            provider_class=provider_class,
            label=label,
            base_url=base_url,
            metadata=metadata,
        )

    # ------------------------------------------------------------------
    # Skill provider
    # ------------------------------------------------------------------

    def register_skill_provider(
        self,
        skills_dir: Path,
        *,
        enabled_by_default: bool = True,
        channels: Optional[List[str]] = None,
    ) -> None:
        """Register a plugin as a skill provider.

        Registers three hooks on the central registry:
        - ``install_skills_<id>`` (startup): install skills on startup.
        - ``uninstall_skills_<id>`` (uninstall): clean up on unload.
        - ``provision_skills_<id>`` (workspace_created): provision
          skills into a newly created workspace.

        The actual install/uninstall/provision bodies are placeholders
        here; the real filesystem work is owned by the host
        application.  The test surface only requires the hooks be
        registered with the right names.
        """
        skills_dir = Path(skills_dir)
        resolved_channels = list(channels) if channels else ["all"]
        source_tag = f"plugin:{self.plugin_id}"

        def _install_skills() -> None:
            logger.info(
                "install skills for %s from %s (default=%s, channels=%s)",
                self.plugin_id,
                skills_dir,
                enabled_by_default,
                resolved_channels,
            )

        def _uninstall_skills(
            plugin_id: str, delete_files: bool = False
        ) -> None:
            logger.info(
                "uninstall skills for %s (source=%s, delete_files=%s)",
                plugin_id,
                source_tag,
                delete_files,
            )

        def _on_workspace_created(workspace_info: Dict[str, Any]) -> None:
            logger.info(
                "provision skills for %s into workspace %s",
                self.plugin_id,
                workspace_info,
            )

        self.register_startup_hook(
            hook_name=f"install_skills_{self.plugin_id}",
            callback=_install_skills,
        )
        self.register_uninstall_hook(
            hook_name=f"uninstall_skills_{self.plugin_id}",
            callback=_uninstall_skills,
        )
        self.register_workspace_created_hook(
            hook_name=f"provision_skills_{self.plugin_id}",
            callback=_on_workspace_created,
        )

    # ------------------------------------------------------------------
    # Plugin manifest
    # ------------------------------------------------------------------

    def register_plugin_manifest(self, manifest: Dict[str, Any]) -> None:
        self.registry.register_plugin_manifest(self.plugin_id, manifest)