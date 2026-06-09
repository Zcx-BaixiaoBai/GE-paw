"""Stub models for alibabacloud_tea_util."""
from __future__ import annotations
from typing import Any


class RuntimeOptions:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
