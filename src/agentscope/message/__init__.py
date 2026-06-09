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

class Base64Source:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class URLSource:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
