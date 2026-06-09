"""Minimal ``Msg``-shaped value object used by gepaw.agents.

The full agentscope.message.Msg has many features (blocks, ToolResultBlock,
TextBlock, multimodal, etc.) but the gepaw.agents tests only ever look at
``msg.metadata`` and ``msg.role`` / ``msg.content``. Keep the surface
narrow on purpose so we do not pull in the agentscope dependency.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Msg:
    """Lightweight message container compatible with the test surface."""

    name: str = ""
    role: str = ""
    content: Any = None
    metadata: dict = field(default_factory=dict)