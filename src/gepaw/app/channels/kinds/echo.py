"""Echo adapter - useful for tests and dev mode.

This adapter does not connect to any external service. It just exposes a
deliver() method that the test code (or future webhook simulator) can call to
inject an IncomingMessage. The reply is logged via the base send().
"""
from __future__ import annotations

from typing import Any, Dict, List

from ..base import ChannelAdapter, IncomingMessage, OutgoingMessage


class EchoAdapter(ChannelAdapter):
    """In-process echo adapter. Useful for unit tests and local dev."""

    kind = "echo"

    def __init__(self, *, account_id: str, org_id: str, name: str, config: Dict[str, Any]):
        super().__init__(account_id=account_id, org_id=org_id, name=name, config=config)
        self._queued: List[IncomingMessage] = []

    def open(self) -> None:
        return

    def close(self) -> None:
        return

    def fetch(self) -> List[IncomingMessage]:
        if not self._queued:
            return []
        out, self._queued = self._queued, []
        return out

    def deliver(self, msg: IncomingMessage) -> None:
        # Stamp our account id so the manager can route the response back.
        msg.raw = dict(msg.raw or {})
        msg.raw["account_id"] = self.account_id
        self._queued.append(msg)

    def send(self, message: OutgoingMessage) -> None:
        # Echo the reply into a per-account log so the test/UI can inspect it.
        log = self.config.setdefault("sent_log", [])
        log.append({
            "external_chat_id": message.external_chat_id,
            "text": message.text,
        })
