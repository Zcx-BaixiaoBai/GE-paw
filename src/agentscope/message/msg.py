"""Stub Msg class for gepaw test isolation.

Mirrors the agentscope surface used by gepaw: ``role``, ``content``,
``metadata``, ``id``, ``name``, ``text()``.
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Union


class Msg:
    """Lightweight stand-in for agentscope.message.Msg."""

    def __init__(
        self,
        name: str,
        content: Union[str, List[Any], None] = None,
        role: str = "user",
        metadata: Optional[Dict[str, Any]] = None,
        id: Optional[str] = None,
        echo: bool = False,
    ) -> None:
        self.id = id or uuid.uuid4().hex
        self.name = name
        self.role = role
        self.metadata = dict(metadata) if metadata else {}
        if isinstance(content, str):
            self.content: List[Any] = [
                {"type": "text", "text": content},
            ]
        elif isinstance(content, list):
            self.content = list(content)
        else:
            self.content = []
        self._echo = echo

    def text(self) -> str:
        parts: list = []
        for block in self.content:
            if isinstance(block, dict):
                t = block.get("text")
                if t:
                    parts.append(str(t))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)

    def __repr__(self) -> str:
        return f"Msg(name={self.name!r}, role={self.role!r})"