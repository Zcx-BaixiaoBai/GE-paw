"""Plugin registry for gepaw.

A small, dependency-free registry that lets plugins contribute prompt
sections. Sections are positioned relative to "host anchors" declared
by gepaw itself (workspace, multimodal, env_context).
"""
from __future__ import annotations

from typing import Any, Callable, List, Optional


_HOST_ANCHORS = frozenset({"workspace", "multimodal", "env_context"})


class PluginRegistry:
    """Singleton registry where plugins register their prompt sections.

    Sections are stored in registration order. Each section is a dict
    with keys: ``plugin_id``, ``name``, ``after`` (host anchor),
    ``agent_id`` (or None to apply to all agents) and ``provider`` (a
    callable taking the agent and returning a string).
    """

    _instance: Optional["PluginRegistry"] = None

    def __new__(cls) -> "PluginRegistry":
        if cls._instance is None:
            inst = super().__new__(cls)
            inst._sections: List[dict] = []
            cls._instance = inst
        return cls._instance

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
        self._sections.append(
            {
                "plugin_id": plugin_id,
                "name": name,
                "after": after,
                "agent_id": agent_id,
                "provider": provider,
            }
        )

    def unregister_plugin(self, plugin_id: str) -> None:
        self._sections = [s for s in self._sections if s["plugin_id"] != plugin_id]

    def get_sections(self, agent_id: str) -> List[dict]:
        """Return sections visible to ``agent_id`` (includes agent_id=None)."""
        return [s for s in self._sections if s["agent_id"] in (None, agent_id)]

    def clear(self) -> None:
        """Remove every section. Intended for tests / hot reload."""
        self._sections = []