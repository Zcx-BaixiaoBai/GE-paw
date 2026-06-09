"""Channel kind registry.

Each IM kind we *advertise* in CHANNEL_KINDS gets a stub adapter that implements
the same lifecycle. The stubs are intentionally minimal — they are wired into
the channel manager so that admin-defined accounts are picked up and the data
path (incoming -> chat_session -> token_usage_log) can be exercised. A real
adapter can be dropped in later without changing the manager.
"""
from __future__ import annotations

from typing import Any, Dict, List, Type

from ...utils.logging import get_logger
from .base import ChannelAdapter, IncomingHandler, IncomingMessage, OutgoingMessage
from .kinds.echo import EchoAdapter
from .kinds.telegram import TelegramAdapter

logger = get_logger("channels.registry")


# All channel kinds that GE-paw supports in v1. Real network adapters
# (telegram, feishu, wecom, ...) reuse the same lifecycle; their bodies can be
# added in kinds/<name>.py and registered below.
CHANNEL_KINDS: List[str] = [
    "telegram", "feishu", "wecom", "dingtalk", "discord",
    "matrix", "mattermost", "mqtt", "onebot", "qq", "echo",
]


_REGISTRY: Dict[str, Type[ChannelAdapter]] = {
    "echo": EchoAdapter,
    "telegram": TelegramAdapter,
    # The remaining kinds fall back to EchoAdapter so the data path still works.
}


def register(kind: str, cls: Type[ChannelAdapter]) -> None:
    _REGISTRY[kind] = cls


def get_adapter_class(kind: str) -> Type[ChannelAdapter]:
    cls = _REGISTRY.get(kind)
    if cls is not None:
        return cls
    # Default: echo-shaped adapter, kind is set via class attribute
    class _Fallback(EchoAdapter):
        pass
    _Fallback.kind = kind
    return _Fallback


def build_adapter(
    kind: str, *, account_id: str, org_id: str, name: str, config: Dict[str, Any]
) -> ChannelAdapter:
    cls = get_adapter_class(kind)
    return cls(account_id=account_id, org_id=org_id, name=name, config=config)


__all__ = [
    "CHANNEL_KINDS",
    "register",
    "get_adapter_class",
    "build_adapter",
    "ChannelAdapter",
    "IncomingMessage",
    "OutgoingMessage",
    "IncomingHandler",
]
