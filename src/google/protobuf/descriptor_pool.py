"""Stub for google.protobuf.descriptor_pool."""
from typing import Any


class DescriptorPool:
    def __init__(self) -> None:
        pass

    def FindMessageTypeByName(self, name: str) -> Any:
        return None

    def Add(self, file_desc) -> None:
        return None


_default = DescriptorPool()


def Default() -> DescriptorPool:
    return _default
