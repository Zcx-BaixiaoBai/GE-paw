"""Stub TokenCounterBase for gepaw test isolation."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Sequence


class TokenCounterBase(ABC):
    """Minimal placeholder matching the real agentscope interface."""

    def __init__(self, *, estimate_divisor: float = 4.0) -> None:
        if estimate_divisor == 0:
            raise ValueError("estimate_divisor cannot be zero")
        self.estimate_divisor = float(estimate_divisor)

    @abstractmethod
    async def count(self, message: object) -> int:
        ...