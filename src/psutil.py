"""Stub for psutil."""
from __future__ import annotations
import os
from typing import Any, List


def pid_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def process_iter(attrs: List[str] = None) -> List['Process']:
    return []


class Process:
    def __init__(self, pid: int = 0) -> None:
        self.pid = pid

    def name(self) -> str:
        return ''

    def cmdline(self) -> List[str]:
        return []

    def ppid(self) -> int:
        return 0

    def parent(self) -> 'Process':
        return Process()

    def children(self, recursive: bool = False) -> List['Process']:
        return []

    def terminate(self) -> None:
        return None

    def kill(self) -> None:
        return None

    def wait(self, timeout: float = None) -> int:
        return 0


def wait_procs(procs: List[Process], timeout: float = None) -> tuple:
    return [], []


def Popen(*args: Any, **kwargs: Any) -> Any:
    return None
