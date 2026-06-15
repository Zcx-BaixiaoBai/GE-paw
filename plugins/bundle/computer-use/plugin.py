"""Computer Use plugin entrypoint.

Registers the four ``computer_*`` tools with the agent runtime. Each tool
is thin by design: the actual platform work happens in the Tauri bridge
(``window.__TAURI_INTERNALS__``). In a non-desktop build the tools
return a structured error so the agent can recover gracefully.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def computer_screenshot(**_: Any) -> Dict[str, Any]:
    """Capture the current screen and return it as a base64 data URL."""
    return {
        "ok": False,
        "reason": "screenshot_bridge_unavailable",
        "hint": "Tauri bridge required for live screenshots; the web UI shows a placeholder.",
    }


def computer_click(x: int, y: int, button: str = "left") -> Dict[str, Any]:
    """Click at absolute screen coordinates."""
    return {
        "ok": False,
        "reason": "input_bridge_unavailable",
        "hint": f"would click ({x},{y}) button={button} when Tauri bridge is present",
    }


def computer_type(text: str) -> Dict[str, Any]:
    """Type the given text into the currently focused input."""
    return {
        "ok": False,
        "reason": "input_bridge_unavailable",
        "hint": f"would type {len(text)} chars when Tauri bridge is present",
    }


def computer_key(combo: str) -> Dict[str, Any]:
    """Press a single key or combination."""
    return {
        "ok": False,
        "reason": "input_bridge_unavailable",
        "hint": f"would press {combo} when Tauri bridge is present",
    }


TOOL_DEFS = [
    {
        "name": "computer_screenshot",
        "func": computer_screenshot,
        "description": "Capture the current screen and return it as a base64 data URL.",
        "icon": "🖥",
        "enabled": False,
    },
    {
        "name": "computer_click",
        "func": computer_click,
        "description": "Click at absolute screen coordinates with the given mouse button.",
        "icon": "🖱",
        "enabled": False,
    },
    {
        "name": "computer_type",
        "func": computer_type,
        "description": "Type the given text into the currently focused input.",
        "icon": "⌨",
        "enabled": False,
    },
    {
        "name": "computer_key",
        "func": computer_key,
        "description": "Press a single key or a combination like 'Return' or 'ctrl+l'.",
        "icon": "⏎",
        "enabled": False,
    },
]


class ComputerUsePlugin:
    """Plugin entrypoint used by gepaw'\''s plugin loader."""

    def register(self, api):
        """Register the four computer_* tools on startup."""

        for tool in TOOL_DEFS:
            try:
                api.register_tool(
                    tool_name=tool["name"],
                    tool_func=tool["func"],
                    description=tool["description"],
                    icon=tool["icon"],
                    enabled=tool["enabled"],
                )
            except Exception as exc:  # pragma: no cover - defensive
                logger.warning("Failed to register tool %s: %s", tool["name"], exc)

        try:
            api.register_startup_hook(
                hook_name="computer_use_init",
                callback=self._on_startup,
                priority=20,
            )
        except Exception:
            logger.info("startup hook already present or unavailable")

        logger.info("Computer use plugin registered (%d tools)", len(TOOL_DEFS))

    async def _on_startup(self):
        logger.info("Computer use plugin ready")


plugin = ComputerUsePlugin()

