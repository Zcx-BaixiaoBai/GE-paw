"""gepaw.plugins: plugin registry and extension points."""
from __future__ import annotations

from .api import PluginApi
from .architecture import PluginEntryPoints, PluginManifest, PluginRecord
from .loader import PluginLoader
from .registry import (
    HookRegistration,
    PluginRegistry,
    ProviderRegistration,
    PromptSectionRegistration,
)
from .validation import validate_plugin_module

__all__ = [
    "HookRegistration",
    "PluginApi",
    "PluginEntryPoints",
    "PluginLoader",
    "PluginManifest",
    "PluginRecord",
    "PluginRegistry",
    "ProviderRegistration",
    "PromptSectionRegistration",
    "validate_plugin_module",
]