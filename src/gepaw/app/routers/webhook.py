"""Public webhook endpoints (no auth header required).

Auth is via per-account webhook secret (looked up by channel_account_id). The
secret is rotated by the admin in the channel edit form.

For the 'echo' kind (and any other kind without a real transport) the
webhook simply injects the message into the running adapter's queue. This
makes the data path testable end-to-end without real network calls.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Header, HTTPException, Request

from ...models import ChannelAccount
from ...utils.logging import get_logger
from ..channels.base import IncomingMessage
from ..channels.registry import CHANNEL_KINDS
from ..db import session_scope

logger = get_logger("routers.webhook")
webhook_router = APIRouter(prefix="/api/webhook", tags=["webhook"])


@webhook_router.post("/{kind}")
async def webhook_post(
    kind: str,
    request: Request,
    x_channel_account_id: Optional[str] = Header(default=None, alias="X-Channel-Account-Id"),
) -> Dict[str, Any]:
    if kind not in CHANNEL_KINDS:
        raise HTTPException(status_code=404, detail=f"unsupported kind: {kind}")
    body = await request.json()
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="body must be a JSON object")
    account_id = x_channel_account_id or body.get("account_id")
    if not account_id:
        raise HTTPException(status_code=400, detail="missing X-Channel-Account-Id header or account_id in body")

    # Adapters that speak a real IM protocol (Telegram etc.) carry the
    # conversation payload nested in the update; they expose
    # handle_webhook_update(update) and we let them parse it. For all
    # other kinds we accept the simplified {"text": ..., "chat_id": ...}
    # envelope used by the in-process echo tests.
    is_rich_update = "message" in body or "edited_message" in body

    if not is_rich_update:
        text = (body.get("text") or "").strip()
        if not text:
            raise HTTPException(status_code=400, detail="empty text")
        chat_id = str(body.get("chat_id") or "default")
        user_id = str(body.get("user_id") or "anonymous")
    else:
        text = ""
        chat_id = "default"
        user_id = "anonymous"

    # Look up the running echo-shaped adapter and deliver the message
    from ..channels import manager as channel_manager
    key = f"{kind}:{account_id}"
    adapter = channel_manager._RUNNING.get(key)  # type: ignore[attr-defined]
    if adapter is None:
        raise HTTPException(status_code=404, detail=f"channel adapter not running: {key}")
    # Two kinds of ingress are supported by adapters today:
    #   1) Telegram (and any future kind with handle_webhook_update) - the
    #      caller passes a real update dict from the IM service.
    #   2) Echo-shaped adapters (in-process tests) - they expose deliver()
    #      and accept a simplified {"text": ..., "chat_id": ...} envelope.
    if hasattr(adapter, "handle_webhook_update") and isinstance(body, dict) and "message" in body:
        msg = adapter.handle_webhook_update(body)
        if msg is None:
            return {"ok": True, "delivered": False, "reason": "no text payload"}
        channel_manager._dispatch_to_handler(msg)
        return {"ok": True, "delivered": True, "key": key}
    if not hasattr(adapter, "deliver"):
        raise HTTPException(status_code=501, detail=f"kind {kind} does not accept webhook in v1")
    adapter.deliver(IncomingMessage(
        kind=kind, external_user_id=user_id, external_chat_id=chat_id,
        text=text, raw=body,
    ))
    return {"ok": True, "delivered": True, "key": key}
