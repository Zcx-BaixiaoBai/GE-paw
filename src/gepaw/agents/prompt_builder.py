"""PromptBuilder: assembles the system prompt from host anchors + plugin sections."""
from __future__ import annotations

import logging
from typing import Any, List, Optional

from gepaw.plugins.registry import PluginRegistry


logger = logging.getLogger(__name__)


class PromptBuilder:
    """Compose the system prompt for an agent.

    Host anchors are visited in the fixed order
    ``workspace -> multimodal -> env_context``. Plugin sections whose
    ``after`` field names one of those anchors are inserted directly
    after it, in registration order. Sections whose ``agent_id`` does
    not match the caller (and is not None) are hidden. Providers that
    return an empty string or raise are skipped silently; raised
    providers additionally log via ``logger.exception``.
    """

    _ANCHOR_ORDER = ("workspace", "multimodal", "env_context")

    def __init__(self, registry: Optional[PluginRegistry] = None) -> None:
        self.registry = registry or PluginRegistry()

    def build(
        self,
        *,
        agent: Any,
        agent_id: str,
        workspace: str = "",
        multimodal: str = "",
        env_context: str = "",
    ) -> str:
        anchors = {
            "workspace": workspace,
            "multimodal": multimodal,
            "env_context": env_context,
        }
        sections = self.registry.get_sections(agent_id)
        by_anchor: dict = {a: [] for a in self._ANCHOR_ORDER}
        for s in sections:
            by_anchor[s["after"]].append(s)

        parts: List[str] = []
        for anchor in self._ANCHOR_ORDER:
            value = anchors[anchor]
            if value:
                parts.append(value)
            for section in by_anchor[anchor]:
                text = self._safe_call(section, agent)
                if text:
                    parts.append(text)
        return "\n\n".join(parts)

    @staticmethod
    def _safe_call(section: dict, agent: Any) -> str:
        provider = section["provider"]
        try:
            text = provider(agent)
        except Exception:  # noqa: BLE001 - prompt section errors are non-fatal
            logger.exception(
                "prompt section %s (plugin=%s) provider raised",
                section.get("name"),
                section.get("plugin_id"),
            )
            return ""
        return text or ""