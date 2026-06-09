"""Stub for Tea.exceptions."""
from __future__ import annotations


class TeaException(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        # The real SDK accepts either kwargs (code/message/data/stackTrace)
        # or a positional `dict`.  We surface the union so callers can
        # read either `.statusCode` (top-level) or `.data.statusCode`.
        data = kwargs.get("data", None)
        if data is None and args and isinstance(args[0], dict):
            data = args[0].get("data")
        self.code = kwargs.get("code", "")
        self.message = kwargs.get("message", "")
        self.data = data
        self.stack_trace = kwargs.get("stackTrace", "")
        # Promote common nested status codes onto the exception itself so
        # gepaw code that does `exc.statusCode == 401` works.
        if isinstance(data, dict) and "statusCode" in data:
            self.statusCode = data["statusCode"]
