"""Stub for google.protobuf.json_format."""
from typing import Any


def Parse(text: str, message: Any) -> Any:
    return message


def MessageToDict(message: Any) -> dict:
    return {}


def MessageToJson(message: Any) -> str:
    return '{}'


def ParseDict(js_dict: dict, message: Any) -> Any:
    return message
