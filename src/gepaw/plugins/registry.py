"""Plugin registry for gepaw.

Central place where plugins contribute:
- prompt sections (host-anchored system prompt fragments)
- startup / shutdown / uninstall / workspace_created hooks
- providers, control commands, plugin manifests, and HTTP routers

Only the methods exercised by the current test surface are
implemented; the rest stay as TODO-free no-ops so callers don't
crash.  The class is a singleton: tests that need isolation should
clear ``PluginRegistry._instance`` and re-instantiate.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


logger = logging.getLogger(__name__)


_HOST_ANCHORS = frozenset({"workspace", "multimodal", "env_context"})


@dataclass
class HookRegistration:
    """Hook registration record."""

    plugin_id: str
    hook_name: str
    callback: Callable
    priority: int = 100


@dataclass
class ProviderRegistration:
    """Provider registration record."""

    plugin_id: str
    provider_id: str
    provider_class: Any
    label: str = ""
    base_url: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PromptSectionRegistration:
    """System-prompt section contributed by a plugin."""

    plugin_id: str
    name: str
    after: str
    agent_id: Optional[str]
    provider: Callable[[Any], str]


class PluginRegistry:
    """Singleton registry where plugins register their extensions."""

    _instance: Optional["PluginRegistry"] = None

    def __new__(cls) -> "PluginRegistry":
        if cls._instance is None:
            inst = super().__new__(cls)
            inst._initialized = False
            cls._instance = inst
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        self._prompt_sections: List[PromptSectionRegistration] = []
        self._startup_hooks: List[HookRegistration] = []
        self._shutdown_hooks: List[HookRegistration] = []
        self._uninstall_hooks: List[HookRegistration] = []
        self._workspace_created_hooks: List[HookRegistration] = []
        self._providers: Dict[str, ProviderRegistration] = {}
        self._plugin_manifests: Dict[str, Dict[str, Any]] = {}
        self._initialized = True

    # ------------------------------------------------------------------
    # Prompt sections
    # ------------------------------------------------------------------

    def register_prompt_section(
        self,
        *,
        plugin_id: str,
        name: str,
        after: str,
        agent_id: Optional[str],
        provider: Callable[[Any], str],
    ) -> None:
        if after not in _HOST_ANCHORS:
            raise ValueError(
                f"after={after!r} must reference a host anchor "
                f"(one of {sorted(_HOST_ANCHORS)})"
            )
        self._prompt_sections.append(
            PromptSectionRegistration(
                plugin_id=plugin_id,
                name=name,
                after=after,
                agent_id=agent_id,
                provider=provider,
            )
        )

    def get_prompt_sections(self, agent_id: str) -> List[PromptSectionRegistration]:
        """Return prompt sections visible to ``agent_id`` (incl. agent_id=None)."""
        return [s for s in self._prompt_sections if s.agent_id in (None, agent_id)]

    # Back-compat alias used by PromptBuilder
    def get_sections(self, agent_id: str) -> List[PromptSectionRegistration]:
        return self.get_prompt_sections(agent_id)

    # ------------------------------------------------------------------
    # Hooks (startup / shutdown / uninstall / workspace_created)
    # ------------------------------------------------------------------

    def register_startup_hook(
        self,
        *,
        plugin_id: str,
        hook_name: str,
        callback: Callable,
        priority: int = 100,
    ) -> None:
        self._startup_hooks.append(
            HookRegistration(plugin_id, hook_name, callback, priority)
        )

    def get_startup_hooks(self) -> List[HookRegistration]:
        return sorted(self._startup_hooks, key=lambda h: h.priority)

    def register_shutdown_hook(
        self,
        *,
        plugin_id: str,
        hook_name: str,
        callback: Callable,
        priority: int = 100,
    ) -> None:
        self._shutdown_hooks.append(
            HookRegistration(plugin_id, hook_name, callback, priority)
        )

    def get_shutdown_hooks(self) -> List[HookRegistration]:
        return sorted(self._shutdown_hooks, key=lambda h: h.priority)

    def register_uninstall_hook(
        self,
        *,
        plugin_id: str,
        hook_name: str,
        callback: Callable,
        priority: int = 100,
    ) -> None:
        self._uninstall_hooks.append(
            HookRegistration(plugin_id, hook_name, callback, priority)
        )

    def get_uninstall_hooks(self, plugin_id: Optional[str] = None) -> List[HookRegistration]:
        hooks = self._uninstall_hooks
        if plugin_id is not None:
            hooks = [h for h in hooks if h.plugin_id == plugin_id]
        return sorted(hooks, key=lambda h: h.priority)

    def register_workspace_created_hook(
        self,
        *,
        plugin_id: str,
        hook_name: str,
        callback: Callable,
        priority: int = 100,
    ) -> None:
        self._workspace_created_hooks.append(
            HookRegistration(plugin_id, hook_name, callback, priority)
        )

    def get_workspace_created_hooks(
        self, plugin_id: Optional[str] = None
    ) -> List[HookRegistration]:
        hooks = self._workspace_created_hooks
        if plugin_id is not None:
            hooks = [h for h in hooks if h.plugin_id == plugin_id]
        return sorted(hooks, key=lambda h: h.priority)

    # ------------------------------------------------------------------
    # Providers
    # ------------------------------------------------------------------

    def register_provider(
        self,
        plugin_id: str,
        provider_id: str,
        provider_class: Any,
        label: str = "",
        base_url: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        if provider_id in self._providers:
            existing = self._providers[provider_id]
            raise ValueError(
                f"Provider '{provider_id}' already registered "
                f"by plugin '{existing.plugin_id}'"
            )
        self._providers[provider_id] = ProviderRegistration(
            plugin_id=plugin_id,
            provider_id=provider_id,
            provider_class=provider_class,
            label=label,
            base_url=base_url,
            metadata=metadata or {},
        )

    def get_providers(self) -> List[ProviderRegistration]:
        return list(self._providers.values())

    # ------------------------------------------------------------------
    # Plugin manifests
    # ------------------------------------------------------------------

    def register_plugin_manifest(
        self, plugin_id: str, manifest: Dict[str, Any]
    ) -> None:
        self._plugin_manifests[plugin_id] = dict(manifest)

    def get_plugin_manifest(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        return self._plugin_manifests.get(plugin_id)

    # ------------------------------------------------------------------
    # Bulk cleanup
    # ------------------------------------------------------------------

    def unregister_plugin(self, plugin_id: str) -> None:
        self._prompt_sections = [
            s for s in self._prompt_sections if s.plugin_id != plugin_id
        ]
        self._startup_hooks = [
            h for h in self._startup_hooks if h.plugin_id != plugin_id
        ]
        self._shutdown_hooks = [
            h for h in self._shutdown_hooks if h.plugin_id != plugin_id
        ]
        self._uninstall_hooks = [
            h for h in self._uninstall_hooks if h.plugin_id != plugin_id
        ]
        self._workspace_created_hooks = [
            h for h in self._workspace_created_hooks if h.plugin_id != plugin_id
        ]
        self._providers = {
            k: v for k, v in self._providers.items() if v.plugin_id != plugin_id
        }
        self._plugin_manifests.pop(plugin_id, None)

    def clear(self) -> None:
        """Drop every registration. Intended for tests / hot reload."""
        self._prompt_sections.clear()
        self._startup_hooks.clear()
        self._shutdown_hooks.clear()
        self._uninstall_hooks.clear()
        self._workspace_created_hooks.clear()
        self._providers.clear()
        self._plugin_manifests.clear()