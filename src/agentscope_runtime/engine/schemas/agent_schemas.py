"""Stub for agentscope_runtime Message schemas."""
from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class MessageType(str, Enum):
    """Enum of supported message types."""

    MESSAGE = "message"
    FUNCTION_CALL = "function_call"
    FUNCTION_CALL_OUTPUT = "function_call_output"
    PLUGIN_CALL = "plugin_call"
    PLUGIN_CALL_OUTPUT = "plugin_call_output"
    MCP_TOOL_CALL = "mcp_tool_call"
    MCP_TOOL_CALL_OUTPUT = "mcp_tool_call_output"


class ContentType(str, Enum):
    """Enum of content block types."""

    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    FILE = "file"
    DATA = "data"


class TextContent(BaseModel):
    """Plain text content."""

    type: ContentType = Field(default=ContentType.TEXT)
    text: str = Field(default="")


class ImageContent(BaseModel):
    """Image content."""

    type: ContentType = Field(default=ContentType.IMAGE)
    image_url: str = Field(default="")


class AudioContent(BaseModel):
    """Audio content."""

    type: ContentType = Field(default=ContentType.AUDIO)
    audio_url: str = Field(default="")


class VideoContent(BaseModel):
    """Video content."""

    type: ContentType = Field(default=ContentType.VIDEO)
    video_url: str = Field(default="")


class FileContent(BaseModel):
    """File content."""

    type: ContentType = Field(default=ContentType.FILE)
    file_url: str = Field(default="")
    filename: str = Field(default="")


class DataContent(BaseModel):
    """Generic structured data content."""

    type: ContentType = Field(default=ContentType.DATA)
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


class AgentRequest(BaseModel):
    """Inbound agent request, used by channel adapters."""

    session_id: str = Field(default="")
    user_id: str = Field(default="")
    channel: str = Field(default="")
    sender_id: Optional[str] = Field(default=None)
    content_parts: List[Any] = Field(default_factory=list)
    text: str = Field(default="")
    metadata: dict = Field(default_factory=dict)
    raw: Any = Field(default=None)

    def model_dump(self, **kwargs):
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "channel": self.channel,
            "sender_id": self.sender_id,
            "content_parts": list(self.content_parts),
            "text": self.text,
            "metadata": dict(self.metadata),
        }


def _type_value(value):
    """Return the underlying value of a ContentType/MessageType member."""
    if isinstance(value, Enum):
        return value.value
    return value
class RunStatus(str, Enum):
    """Status of an agent run."""

    Created = "created"
    InProgress = "in_progress"
    Completed = "completed"
    Failed = "failed"
    Canceled = "canceled"
    Rejected = "rejected"
    Unknown = "unknown"


class RefusalContent(BaseModel):
    """Refusal content block."""

    type: ContentType = Field(default=ContentType.TEXT)
    refusal: str = Field(default="")


class AgentResponse(BaseModel):
    """Outbound agent response."""

    session_id: str = Field(default="")
    run_id: str = Field(default="")
    status: RunStatus = Field(default=RunStatus.Created)
    content_parts: List[Any] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)

    def model_dump(self, **kwargs):
        return {
            "session_id": self.session_id,
            "run_id": self.run_id,
            "status": self.status.value if isinstance(self.status, RunStatus) else self.status,
            "content_parts": list(self.content_parts),
            "metadata": dict(self.metadata),
        }


class Usage(BaseModel):
    """Token usage stats."""

    input_tokens: int = Field(default=0)
    output_tokens: int = Field(default=0)


class SessionInfo(BaseModel):
    """Session metadata returned by the runtime."""

    session_id: str = Field(default="")
    user_id: str = Field(default="")
    channel: str = Field(default="")