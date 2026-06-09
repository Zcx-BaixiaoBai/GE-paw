"""Stub for Tea.exceptions."""
from __future__ import annotations


class TeaException(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        self.code = kwargs.get("code", "")
        self.message = kwargs.get("message", "")
        self.data = kwargs.get("data", None)
        self.stack_trace = kwargs.get("stackTrace", "")
