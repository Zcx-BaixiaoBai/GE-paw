"""Stub: ChatResponse for gepaw test isolation."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ChatResponse:
    """Minimal response shape used by gepaw tests."""

    content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    usage: Optional[Dict[str, Any]] = None
    id: Optional[str] = None
    finish_reason: Optional[str] = None