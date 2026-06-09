"""Channel adapter base class.

A channel adapter is responsible for opening a long-lived connection to an
external IM service (Telegram, Feishu, WeCom, ...), receiving user messages,
forwarding them to the assistant agent, and posting the reply back.

The base class provides the lifecycle and a default in-memory polling loop.
Concrete kinds override open() / fetch() / send() as needed.

For kinds we have not actually wired to a public API, the registry provides a
EchoAdapter that simply logs the message and returns a canned reply. This
keeps the data path (incoming message -> chat_session -> token_usage_log)
exercised end-to-end even in development.
"""
from __future__ import annotations

import abc
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from ...utils.logging import get_logger

logger = get_logger("channels.base")


@dataclass
class IncomingMessage:
    """A message received from a channel."""
    kind: str
    external_user_id: str
    external_chat_id: str
    text: str
    raw: Dict[str, Any] = field(default_factory=dict)
    received_at: float = field(default_factory=time.time)


@dataclass
class OutgoingMessage:
    """A reply to be sent back to the channel."""
    kind: str
    external_chat_id: str
    text: str
    extra: Dict[str, Any] = field(default_factory=dict)


# A handler takes an IncomingMessage and returns either an OutgoingMessage
# or a plain text reply. It is provided by the channel manager.
IncomingHandler = Callable[[IncomingMessage], Optional[OutgoingMessage]]


class ChannelAdapter(abc.ABC):
    """Base class for channel adapters."""

    kind: str = "base"

    def __init__(self, *, account_id: str, org_id: str, name: str, config: Dict[str, Any]):
        self.account_id = account_id
        self.org_id = org_id
        self.name = name
        self.config = dict(config or {})
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._handler: Optional[IncomingHandler] = None

    def bind(self, handler: IncomingHandler) -> None:
        self._handler = handler

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        try:
            self.open()
        except Exception as e:
            logger.warning("channel %s open failed: %s", self.kind, e)
        self._thread = threading.Thread(
            target=self._run_loop, name=f"channel-{self.kind}-{self.name}", daemon=True
        )
        self._thread.start()
        logger.info("channel %s (%s) started for org %s", self.kind, self.name, self.org_id)

    def stop(self) -> None:
        self._stop_event.set()
        try:
            self.close()
        except Exception as e:
            logger.warning("channel %s close failed: %s", self.kind, e)
        if self._thread is not None:
            self._thread.join(timeout=2.0)
            self._thread = None
        logger.info("channel %s (%s) stopped", self.kind, self.name)

    @abc.abstractmethod
    def open(self) -> None:
        ...

    @abc.abstractmethod
    def close(self) -> None:
        ...

    def fetch(self) -> List[IncomingMessage]:
        """Return any new messages since last call. Default: none."""
        return []

    def send(self, message: OutgoingMessage) -> None:
        """Send a reply. Default: log only."""
        logger.info(
            "channel %s reply -> chat %s: %s",
            self.kind, message.external_chat_id, (message.text or "")[:200],
        )

    def _run_loop(self) -> None:
        handler = self._handler
        while not self._stop_event.is_set():
            try:
                for msg in self.fetch():
                    if handler is None:
                        logger.warning("no handler bound for channel %s", self.kind)
                        continue
                    try:
                        reply = handler(msg)
                    except Exception as e:
                        logger.exception("handler error: %s", e)
                        continue
                    if reply is None:
                        continue
                    try:
                        self.send(reply)
                    except Exception as e:
                        logger.warning("send failed: %s", e)
            except Exception as e:
                logger.warning("channel %s loop error: %s", self.kind, e)
            # poll interval
            self._stop_event.wait(self._poll_interval())

    def _poll_interval(self) -> float:
        return float(self.config.get("poll_interval", 2.0))
