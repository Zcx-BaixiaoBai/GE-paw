"""Stub for google.protobuf.descriptor_pb2 with FileDescriptorProto."""
from typing import Any


class FileDescriptorProto:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def ParseFromString(self, data: bytes) -> int:
        return 0

    def SerializeToString(self) -> bytes:
        return b''


class FieldDescriptorProto:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class DescriptorProto:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
