"""Stub for google.protobuf.descriptor."""
from typing import Any


class FieldDescriptor:
    pass


class Descriptor:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def fields_by_name(self) -> dict:
        return {}


class FileDescriptor:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
