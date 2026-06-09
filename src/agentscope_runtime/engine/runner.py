"""Stub for agentscope_runtime.engine.runner."""
from __future__ import annotations
from typing import Any


class Runner:
    """Stub for `agentscope_runtime.engine.runner.Runner`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    async def run(self, *args: Any, **kwargs: Any) -> Any:
        return None

    async def stream(self, *args: Any, **kwargs: Any) -> Any:
        yield None

    async def stop(self) -> None:
        return None

    async def close(self) -> None:
        return None
