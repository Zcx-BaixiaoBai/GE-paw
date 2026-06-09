"""Abstract base class for all tool-call guardians.

Every concrete guardian must subclass :class:`BaseToolGuardian` and
implement :meth:`guard`.  The interface is intentionally minimal so
new detection engines (e.g. LLM-based, semantic analysis) can be added
as drop-in plugins without touching the guard engine.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List

from ..models import GuardFinding


class BaseToolGuardian(ABC):
    """Abstract base class for all tool-call guardians.

    Parameters
    ----------
    name:
        Human-readable guardian name (used in
        :attr:`GuardFinding.guardian`).
    always_run:
        When True, the engine runs this guardian even for tools not
        listed in the guarded set.  Useful for global scanners like
        path-traversal checks.
    """

    def __init__(self, name: str, *, always_run: bool = False) -> None:
        self.name = name
        self.always_run = always_run

    @abstractmethod
    def guard(
        self,
        tool_name: str,
        params: dict,
    ) -> List[GuardFinding]:
        """Guard the parameters of a tool call for security issues.

        Returns a (possibly empty) list of findings.
        """

    def __repr__(self) -> str:
        return f"<{type(self).__name__} name={self.name!r}>"