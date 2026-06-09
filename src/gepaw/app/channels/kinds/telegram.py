"""Telegram Bot API adapter (long polling).

Uses the official Bot API over HTTPS via urllib (no extra dependency). The
adapter keeps a long-lived polling thread; the manager binds a handler that
turns each update into a ChatSession round-trip.

Configuration:
    bot_token   - BotFather token, required. Can also be supplied via the
                  encrypted credentials blob stored on ChannelAccount.
    poll_timeout - Long-poll timeout in seconds, default 25.
    api_base    - Override for tests, default https://api.telegram.org.

This is a v1 implementation: text only, no inline keyboards, no media. Adding
those later is a matter of expanding the send() payload and parsing
additional update fields; the lifecycle stays the same.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ....utils.logging import get_logger
from ..base import ChannelAdapter, IncomingMessage, OutgoingMessage

logger = get_logger("channels.telegram")

API_DEFAULT = "https://api.telegram.org"
MAX_TEXT = 4000  # Telegram hard limit is 4096; keep some headroom.


class TelegramAdapter(ChannelAdapter):
    """Long-polling Telegram Bot adapter."""

    kind = "telegram"

    def __init__(self, *, account_id: str, org_id: str, name: str, config: Dict[str, Any]):
        super().__init__(account_id=account_id, org_id=org_id, name=name, config=config)
        self._offset: Optional[int] = None
        self._bot_token: Optional[str] = None
        self._api_base: str = str(self.config.get("api_base") or API_DEFAULT)
        self._poll_timeout: int = int(self.config.get("poll_timeout", 25))

    # --- lifecycle -------------------------------------------------------

    def open(self) -> None:
        token = self.config.get("bot_token")
        if not token:
            raise RuntimeError(
                f"telegram adapter {self.name!r} is missing bot_token",
            )
        self._bot_token = str(token)
        # Verify the token once so misconfiguration fails fast.
        try:
            self._call("getMe", http_timeout=5)
        except Exception as e:  # pragma: no cover - network path
            logger.warning("telegram getMe failed for %s: %s", self.name, e)

    def close(self) -> None:
        return

    # --- polling ---------------------------------------------------------

    def _call(self, method: str, *, http_timeout: int = 10, **params: Any) -> Dict[str, Any]:
        if not self._bot_token:
            raise RuntimeError("bot_token not initialised")
        url = f"{self._api_base.rstrip('/')}/bot{self._bot_token}/{method}"
        if params:
            url += "?" + urllib.parse.urlencode(params, doseq=True)
        req = urllib.request.Request(url, headers={"User-Agent": "GE-paw/0.1"})
        with urllib.request.urlopen(req, timeout=http_timeout) as resp:  # noqa: S310
            body = resp.read().decode("utf-8", errors="replace")
        data = json.loads(body)
        if not data.get("ok", False):
            raise RuntimeError(f"telegram {method} returned ok=false: {data}")
        return data

    def fetch(self) -> List[IncomingMessage]:
        # Note: Telegram's "timeout" param is the long-poll wait, while the
        # urllib timeout is the socket read deadline. We pass the former via
        # the query string and pick the latter as a small multiple.
        params: Dict[str, Any] = {"timeout": self._poll_timeout, "allowed_updates": json.dumps(["message"])}
        if self._offset is not None:
            params["offset"] = self._offset
        try:
            data = self._call("getUpdates", http_timeout=self._poll_timeout + 10, **params)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, RuntimeError) as e:
            logger.warning("telegram getUpdates failed for %s: %s", self.name, e)
            # Back off a touch so we don't hammer a flaky network
            time.sleep(min(5.0, float(self.config.get("error_backoff", 2.0))))
            return []

        results = data.get("result") or []
        out: List[IncomingMessage] = []
        for upd in results:
            try:
                upd_id = int(upd["update_id"])
            except (KeyError, TypeError, ValueError):
                continue
            self._offset = max(self._offset or 0, upd_id + 1)
            msg = upd.get("message") or upd.get("edited_message")
            if not msg:
                continue
            chat = msg.get("chat") or {}
            chat_id = chat.get("id")
            if chat_id is None:
                continue
            from_user = msg.get("from") or {}
            user_id = str(from_user.get("id") or chat_id)
            text = msg.get("text") or msg.get("caption") or ""
            if not text:
                # We do not handle media in v1; surface a hint in the log so
                # admins can see the bot is alive but skipping non-text msgs.
                logger.info(
                    "telegram %s: skipping non-text update %s",
                    self.name, upd_id,
                )
                continue
            im = IncomingMessage(
                kind=self.kind,
                external_user_id=user_id,
                external_chat_id=str(chat_id),
                text=str(text),
                raw={
                    "account_id": self.account_id,
                    "update_id": upd_id,
                    "message_id": msg.get("message_id"),
                    "username": from_user.get("username"),
                },
            )
            out.append(im)
        return out

    # --- sending ---------------------------------------------------------

    def send(self, message: OutgoingMessage) -> None:
        if not self._bot_token:
            logger.warning("telegram %s: send called before open()", self.name)
            return
        text = message.text or ""
        # Telegram has a 4096 char limit; split if needed.
        chunks = [text[i : i + MAX_TEXT] for i in range(0, len(text), MAX_TEXT)] or [""]
        for idx, chunk in enumerate(chunks):
            try:
                self._call(
                    "sendMessage",
                    http_timeout=10,
                    chat_id=str(message.external_chat_id),
                    text=chunk,
                )
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, RuntimeError) as e:
                logger.warning("telegram sendMessage chunk %d failed: %s", idx, e)
                return

    # --- webhook ingress ------------------------------------------------

    def handle_webhook_update(self, update: Dict[str, Any]) -> Optional[IncomingMessage]:
        """Accept a single Telegram update dict (e.g. from a webhook receiver)
        and turn it into an IncomingMessage. Returns None if the update has
        no usable text payload. The webhook router is responsible for calling
        the manager handler with the returned message.
        """
        try:
            upd_id = int(update.get("update_id", 0))
        except (TypeError, ValueError):
            upd_id = 0
        if upd_id:
            self._offset = max(self._offset or 0, upd_id + 1)
        msg = update.get("message") or update.get("edited_message")
        if not msg:
            return None
        chat = msg.get("chat") or {}
        chat_id = chat.get("id")
        if chat_id is None:
            return None
        from_user = msg.get("from") or {}
        user_id = str(from_user.get("id") or chat_id)
        text = msg.get("text") or msg.get("caption") or ""
        if not text:
            return None
        return IncomingMessage(
            kind=self.kind,
            external_user_id=user_id,
            external_chat_id=str(chat_id),
            text=str(text),
            raw={
                "account_id": self.account_id,
                "update_id": upd_id,
                "message_id": msg.get("message_id"),
                "username": from_user.get("username"),
            },
        )

    # --- polling interval ------------------------------------------------

    def _poll_interval(self) -> float:
        # Long polling already blocks up to `_poll_timeout`; the loop is fast.
        # Keep a small floor in case getUpdates returns early.
        return 0.5


__all__ = ["TelegramAdapter"]
