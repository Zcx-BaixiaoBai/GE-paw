"""Stub Msg class for gepaw test isolation.

Mirrors the agentscope surface used by gepaw: ``role``, ``content``,
``metadata``, ``id``, ``name``, ``text()``, ``to_dict()``, ``from_dict()``,
``get_content_blocks()``.
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, List, Optional, Union


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
        timestamp: Optional[str] = None,
    ) -> None:
        self.id = id or uuid.uuid4().hex
        self.name = name
        self.role = role
        self.metadata = dict(metadata) if metadata else {}
        self.timestamp = timestamp or ""
        # Preserve the original type: if a string was passed in, keep it as
        # a string. tests assert ``msg.content == "..."`` for plain text
        # messages.  Iteration helpers normalise on the fly.
        if isinstance(content, str):
            self.content: Union[str, List[Any]] = content
        elif isinstance(content, list):
            self.content = list(content)
        else:
            self.content = []
        self._echo = echo

    def text(self) -> str:
        parts: list = []
        if isinstance(self.content, str):
            return self.content
        for block in self.content:
            if isinstance(block, dict):
                t = block.get("text")
                if t:
                    parts.append(str(t))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)

    def get_content_blocks(
        self,
        block_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Return content blocks, optionally filtered by ``block_type``."""
        if isinstance(self.content, str):
            return []
        if block_type is None:
            return [b for b in self.content if isinstance(b, dict)]
        return [
            b for b in self.content
            if isinstance(b, dict) and b.get("type") == block_type
        ]

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the message to a JSON-friendly dict."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "content": _deep_copy_content(self.content),
            "metadata": dict(self.metadata),
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Msg":
        """Build a ``Msg`` from a dict produced by :meth:`to_dict`."""
        msg = cls(
            name=payload.get("name", ""),
            role=payload.get("role", "user"),
            content=payload.get("content", []),
            metadata=payload.get("metadata", {}) or {},
            id=payload.get("id"),
            timestamp=payload.get("timestamp") or None,
        )
        return msg

    def __repr__(self) -> str:
        return f"Msg(name={self.name!r}, role={self.role!r})"


def _deep_copy_content(content):
    """Copy a content list deeply enough to avoid shared references."""
    if isinstance(content, str):
        return content
    out = []
    for block in content:
        if isinstance(block, dict):
            out.append(dict(block))
        elif isinstance(block, list):
            out.append(_deep_copy_content(block))
        else:
            out.append(block)
    return out


class ToolResultBlock(dict):
    """Stub for ``agentscope.message.ToolResultBlock``."""

    def __init__(self, type: str = "tool_result", **kwargs: Any) -> None:
        super().__init__(type=type, **kwargs)