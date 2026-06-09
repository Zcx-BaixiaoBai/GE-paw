"""Stub for google.protobuf.message_factory."""
from typing import Any


def GetMessageClass(descriptor: Any) -> Any:
    class _Msg:
        def __init__(self, *a, **kw):
            for k, v in kw.items():
                setattr(self, k, v)
    return _Msg


def GetPrototype(descriptor: Any) -> Any:
    return None
