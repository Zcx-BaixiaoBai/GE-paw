"""Stub for agentscope_runtime Message schemas."""
from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class MessageType(str, Enum):
    """Enum of supported message types."""

    MESSAGE = "message"
    FUNCTION_CALL = "function_call"
    FUNCTION_CALL_OUTPUT = "function_call_output"


class TextContent(BaseModel):
    """Plain text content."""

    type: str = Field(default="text")
    text: str = Field(default="")


class ImageContent(BaseModel):
    """Image content."""

    type: str = Field(default="image")
    image_url: str = Field(default="")


class AudioContent(BaseModel):
    """Audio content."""

    type: str = Field(default="audio")
    audio_url: str = Field(default="")


class VideoContent(BaseModel):
    """Video content."""

    type: str = Field(default="video")
    video_url: str = Field(default="")


class FileContent(BaseModel):
    """File content."""

    type: str = Field(default="file")
    file_url: str = Field(default="")
    filename: str = Field(default="")


class DataContent(BaseModel):
    """Generic structured data content."""

    type: str = Field(default="data")
    data: Any = Field(default=None)


class FunctionCall(BaseModel):
    """Function-call request."""

    type: str = Field(default="function_call")
    id: str = Field(default="")
    name: str = Field(default="")
    arguments: str = Field(default="")


class FunctionCallOutput(BaseModel):
    """Function-call output."""

    type: str = Field(default="function_call_output")
    call_id: str = Field(default="")
    output: str = Field(default="")


class Message(BaseModel):
    """Lightweight stand-in for ``agentscope_runtime Message``."""

    type: MessageType = Field(default=MessageType.MESSAGE)
    role: str = Field(default="user")
    content: Any = Field(default=None)
    metadata: dict = Field(default_factory=dict)

    def model_dump(self, **kwargs):
        return {
            "type": (
                self.type.value
                if isinstance(self.type, MessageType)
                else self.type
            ),
            "role": self.role,
            "content": self.content,
            "metadata": dict(self.metadata),
        }