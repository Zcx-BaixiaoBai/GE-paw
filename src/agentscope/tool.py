"""Stub for agentscope.tool."""
from __future__ import annotations
from typing import Any


async def execute_python_code(*args, **kwargs) -> Any:
    return ''


async def view_text_file(*args, **kwargs) -> Any:
    return ''


async def write_text_file(*args, **kwargs) -> Any:
    return ''


class Toolkit:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.tools: list = []

    def register_tool_function(self, func) -> None:
        self.tools.append(func)

    def get_json_schemas(self) -> list:
        schemas: list = []
        for func in self.tools:
            name = getattr(func, "__name__", "") or ""
            doc = (getattr(func, "__doc__", "") or "").strip()
            schemas.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": doc,
                    "parameters": {"type": "object", "properties": {}},
                },
            })
        return schemas


class ToolResponse:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._data = dict(kwargs)
        self.content = kwargs.get('content', '')

    def to_dict(self) -> dict:
        return dict(self._data)
