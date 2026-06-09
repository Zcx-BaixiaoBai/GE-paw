"""Stub: minimal agentscope.message for gepaw test isolation."""
from .blocks import (
    AudioBlock,
    ImageBlock,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
    VideoBlock,
)
from .msg import Msg

__all__ = [
    "AudioBlock",
    "ImageBlock",
    "Msg",
    "TextBlock",
    "ToolResultBlock",
    "ToolUseBlock",
    "VideoBlock",
]