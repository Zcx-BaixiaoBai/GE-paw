"""Stub: agentscope.message block types for gepaw test isolation."""
from __future__ import annotations

from typing import Any


class TextBlock(dict):
    """Stub for ``agentscope.message.TextBlock`` (dict subclass)."""

    def __init__(self, type: str = "text", **kwargs: Any) -> None:
        super().__init__(type=type, **kwargs)


class ImageBlock(dict):
    """Stub for ``agentscope.message.ImageBlock`` (dict subclass)."""

    def __init__(self, type: str = "image", **kwargs: Any) -> None:
        super().__init__(type=type, **kwargs)


class AudioBlock(dict):
    """Stub for ``agentscope.message.AudioBlock`` (dict subclass)."""

    def __init__(self, type: str = "audio", **kwargs: Any) -> None:
        super().__init__(type=type, **kwargs)


class VideoBlock(dict):
    """Stub for ``agentscope.message.VideoBlock`` (dict subclass)."""

    def __init__(self, type: str = "video", **kwargs: Any) -> None:
        super().__init__(type=type, **kwargs)


class ToolUseBlock(dict):
    """Stub for ``agentscope.message.ToolUseBlock``."""

    def __init__(self, type: str = "tool_use", **kwargs: Any) -> None:
        super().__init__(type=type, **kwargs)


class ToolResultBlock(dict):
    """Stub for ``agentscope.message.ToolResultBlock``."""

    def __init__(self, type: str = "tool_result", **kwargs: Any) -> None:
        super().__init__(type=type, **kwargs)