"""Stub for acp (Agent Client Protocol) library."""
from __future__ import annotations
from typing import Any


class Agent:
    pass


class Client:
    pass


class InitializeResponse:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class LoadSessionResponse:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class NewSessionResponse:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class PromptResponse:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class SetSessionModelResponse:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


def run_agent(*args: Any, **kwargs: Any) -> Any:
    return None


def start_tool_call(*args: Any, **kwargs: Any) -> Any:
    return None


def update_tool_call(*args: Any, **kwargs: Any) -> Any:
    return None


def text_block(*args: Any, **kwargs: Any) -> Any:
    return None


def tool_content(*args: Any, **kwargs: Any) -> Any:
    return None


def update_agent_message(*args: Any, **kwargs: Any) -> Any:
    return None


def update_agent_thought(*args: Any, **kwargs: Any) -> Any:
    return None


def connect(*args: Any, **kwargs: Any) -> Any:
    return None


PROTOCOL_VERSION = 1


def spawn_agent_process(*args, **kwargs) -> Any:
    return None


def list_sessions(*args, **kwargs) -> Any:
    return []


def create_session(*args, **kwargs) -> Any:
    return None


def kill_process(*args, **kwargs) -> Any:
    return None


class RequestError(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        for k, v in kwargs.items():
            setattr(self, k, v)


class AuthenticationRequired(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        for k, v in kwargs.items():
            setattr(self, k, v)


class PermissionDenied(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        for k, v in kwargs.items():
            setattr(self, k, v)


class McpError(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        for k, v in kwargs.items():
            setattr(self, k, v)


def session_notification(*args, **kwargs) -> Any:
    return None


def request_permission(*args, **kwargs) -> Any:
    return None


def ext_method(*args, **kwargs) -> Any:
    return None
