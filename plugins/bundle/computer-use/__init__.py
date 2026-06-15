"""Computer Use plugin for GE-paw.

Exposes four agent-callable tools that let the model take over the
local screen:

- computer_screenshot() -> data URL
- computer_click(x, y, button="left")
- computer_type(text)
- computer_key(combo)

In desktop builds (Tauri) the heavy lifting happens through the Tauri
bridge (``__TAURI__`` global). In browser builds the tools degrade to
no-ops with a helpful error so the plugin still loads cleanly.
"""

from .plugin import plugin  # noqa: F401

__all__ = ["plugin"]
