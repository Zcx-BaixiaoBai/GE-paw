"""Stub: agentscope.tool for gepaw test isolation."""
from __future__ import annotations

import inspect
from typing import Any


class ToolResponse:
    """Stub for ``agentscope.tool.ToolResponse``.

    The real class is a thin wrapper around a content list. The stub
    exposes ``content`` as both an attribute and a dict-like key so
    tests can use either ``resp.content`` or ``resp["content"]``.
    """

    def __init__(self, content=None, **kwargs: Any) -> None:
        self.content = content if content is not None else []
        # Mirror common fields as dict-like access for downstream code.
        self._data: dict = {"content": self.content, **kwargs}
        for k, v in self._data.items():
            setattr(self, k, v)

    def __getitem__(self, key: str):
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value
        setattr(self, key, value)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def get(self, key: str, default: Any = None):
        return self._data.get(key, default)


class Toolkit:
    """Stub for ``agentscope.tool.Toolkit`` (register tools, dump schemas)."""

    def __init__(self) -> None:
        self.tools: dict = {}

    def register_tool_function(self, func) -> None:
        self.tools[func.__name__] = func

    def get_json_schemas(self) -> list:
        """Return JSON schema dicts for every registered tool function."""
        schemas: list = []
        for name, func in self.tools.items():
            try:
                sig = inspect.signature(func)
            except (TypeError, ValueError):
                sig = None
            params: dict = {}
            required: list = []
            if sig is not None:
                for pname, param in sig.parameters.items():
                    if pname == "self":
                        continue
                    annotation = (
                        str(param.annotation)
                        if param.annotation is not inspect.Parameter.empty
                        else "string"
                    )
                    params[pname] = {"type": annotation}
                    if param.default is inspect.Parameter.empty:
                        required.append(pname)
            schemas.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": (func.__doc__ or "").strip().split("\n")[0],
                    "parameters": {
                        "type": "object",
                        "properties": params,
                        "required": required,
                    },
                },
            })
        return schemas


# Placeholder async tool implementations - tests don't use these directly,
# but they are part of the upstream ``agentscope.tool`` namespace.
async def execute_python_code(*_args, **_kwargs):  # pragma: no cover
    raise NotImplementedError


async def view_text_file(*_args, **_kwargs):  # pragma: no cover
    raise NotImplementedError


async def write_text_file(*_args, **_kwargs):  # pragma: no cover
    raise NotImplementedError


__all__ = [
    "ToolResponse",
    "Toolkit",
    "execute_python_code",
    "view_text_file",
    "write_text_file",
]