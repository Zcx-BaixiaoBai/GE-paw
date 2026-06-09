"""Abstract base for per-agent memory managers.

Subclasses implement the actual LLM / vector-store interactions; the
base only owns the small bookkeeping that the gepaw agents share:
- the background summarization worker state
- the task counter and ``_summary_task_info`` snapshot
- a thin ``add_summarize_task`` / ``list_summarize_status`` pair that
  tests can exercise without standing up a real LLM.
"""
from __future__ import annotations

import asyncio
import time
import uuid
from abc import ABC, abstractmethod
from typing import Any, Iterable


class BaseMemoryManager(ABC):
    """Subclass and implement the abstract methods to plug in a backend."""

    def __init__(self, working_dir: str, agent_id: str) -> None:
        self.working_dir = working_dir
        self.agent_id = agent_id
        self._summary_task_info: dict = {}
        self._task_counter: int = 0
        self._worker_task: asyncio.Task | None = None

    # ------------------------------------------------------------------
    # Backend contract
    # ------------------------------------------------------------------

    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def close(self) -> bool: ...

    @abstractmethod
    def get_memory_prompt(self, language: str = "zh") -> str: ...

    @abstractmethod
    def list_memory_tools(self) -> list: ...

    # The remaining hooks are not abstract so older test code can subclass
    # with only the four above; concrete managers are free to override.

    async def compact_tool_result(self, **_kwargs) -> None:
        return None

    async def check_context(self, **_kwargs):
        return ([], [], True)

    async def compact_memory(self, _messages, **_kwargs) -> str:
        return ""

    async def summary_memory(self, _messages, **_kwargs) -> str:
        return ""

    async def memory_search(self, _query, **_kwargs):
        return None

    def get_in_memory_memory(self, **_kwargs):
        return None

    # ------------------------------------------------------------------
    # Summarization task tracking
    # ------------------------------------------------------------------

    def add_summarize_task(self, _messages: Iterable[Any]) -> str:
        """Register a new summarization task and start the worker if needed.

        The default implementation does not call any LLM; it only
        records the task in ``_summary_task_info`` so the status
        snapshot and counter behave as the tests expect. Concrete
        managers may extend this to actually schedule ``summary_memory``.
        """
        self._task_counter += 1
        task_id = f"sum-{self._task_counter}-{uuid.uuid4().hex[:6]}"
        self._summary_task_info[task_id] = {
            "task_id": task_id,
            "start_time": time.time(),
            "status": "pending",
            "result": None,
            "error": None,
        }
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._summarize_worker())
        return task_id

    async def _summarize_worker(self) -> None:
        """Drain the task queue. The default is a no-op loop."""
        try:
            while True:
                await asyncio.sleep(60)
                if not any(
                    info.get("status") == "pending"
                    for info in self._summary_task_info.values()
                ):
                    return
        except asyncio.CancelledError:
            return

    def list_summarize_status(self) -> list:
        """Return a JSON-serializable snapshot of the current tasks."""
        return [dict(info) for info in self._summary_task_info.values()]