"""Channel manager: starts/stops channel adapters, dispatches messages.

Lifecycle:
    start_all()    - called from FastAPI lifespan; reads all enabled accounts
                    from the database and starts a thread per adapter.
    reload()       - stops everything and re-reads accounts (call after admin
                    creates/deletes/updates a channel).
    stop_all()     - graceful shutdown.

The default IncomingHandler routes messages to the assistant agent via
wiki.llm_client.chat_for_org, which records token usage automatically. The
ChatSession row is created on demand with channel_kind/channel_account_id set
so the admin can see which sessions came from which channel.
"""
from __future__ import annotations

import json
import threading
from typing import Any, Dict, List, Optional

from ...constant import PROJECT_NAME
from ...models import ChatSession, ChannelAccount, Message
from ...utils.logging import get_logger
from ...wiki.llm_client import chat_for_org
from ..db import session_scope
from .base import ChannelAdapter, IncomingMessage, OutgoingMessage
from .registry import CHANNEL_KINDS, build_adapter

logger = get_logger("channels.manager")

_RUNNING: Dict[str, ChannelAdapter] = {}
_LOCK = threading.Lock()


def _make_session_id() -> str:
    import uuid
    return uuid.uuid4().hex


def _load_accounts() -> List[ChannelAccount]:
    """Read all enabled channel accounts from the database."""
    with session_scope() as db:
        rows = (
            db.query(ChannelAccount)
            .filter(ChannelAccount.enabled == True)  # noqa: E712
            .order_by(ChannelAccount.created_at.asc())
            .all()
        )
        # Detach from session; we only read scalar fields below.
        for r in rows:
            db.expunge(r)
        return rows


def _decrypt_credentials(credentials_enc: str) -> Dict[str, Any]:
    if not credentials_enc:
        return {}
    try:
        from ...security.crypto import decrypt
        raw = decrypt(credentials_enc)
        if not raw:
            return {}
        return json.loads(raw)
    except Exception as e:
        logger.warning("decrypt credentials failed: %s", e)
        return {}


def _handle_incoming(msg: IncomingMessage) -> Optional[OutgoingMessage]:
    """Default handler: find or create a ChatSession and call the agent."""
    with session_scope() as db:
        # Look up the running adapter by kind + account_id.
        account_id = (msg.raw or {}).get("account_id")
        adapter = _RUNNING.get(f"{msg.kind}:{account_id}") if account_id else None
        if adapter is None:
            logger.warning("incoming message for unknown adapter %s/%s", msg.kind, account_id)
            return None
        org_id = adapter.org_id

        # Cross-channel routing strategy is controlled by Org.cross_channel_merge:
        #   False (default): sessions are isolated per (channel_kind, account_id, external_chat_id).
        #   True:           sessions are merged across all channels for the same external_chat_id;
        #                   channel_kind/channel_account_id on the session are updated to the most
        #                   recent source so the admin can still see where traffic is coming from.
        from ...models import Org as _Org
        org_row = db.get(_Org, org_id)
        cross_channel_merge = bool(getattr(org_row, "cross_channel_merge", False)) if org_row else False

        q = db.query(ChatSession).filter(
            ChatSession.org_id == org_id,
            ChatSession.title == f"#{msg.external_chat_id}",
            ChatSession.archived == False,  # noqa: E712
        )
        if not cross_channel_merge:
            q = q.filter(
                ChatSession.channel_kind == msg.kind,
                ChatSession.channel_account_id == adapter.account_id,
            )
        sess = q.order_by(ChatSession.created_at.desc()).first()
        if sess is None:
            sess = ChatSession(
                org_id=org_id,
                user_id=_get_system_user_id(db, org_id),
                title=f"#{msg.external_chat_id}",
                channel_kind=msg.kind,
                channel_account_id=adapter.account_id,
                status="active",
            )
            db.add(sess)
            db.flush()
        elif cross_channel_merge:
            # Merge mode: stamp the session with the most recent source so the admin
            # dashboard can tell where the latest message came from.
            sess.channel_kind = msg.kind
            sess.channel_account_id = adapter.account_id
            db.flush()

        # Persist the user message
        user_msg = Message(session_id=sess.id, role="user", content=msg.text or "")
        db.add(user_msg)
        db.flush()

        # Build history from this session
        history_rows = (
            db.query(Message)
            .filter(Message.session_id == sess.id)
            .order_by(Message.created_at.asc())
            .all()
        )
        msgs = [
            {"role": "system", "content": f"You are the {PROJECT_NAME} assistant answering over {msg.kind}."}
        ]
        for m in history_rows:
            role = m.role
            if role not in ("user", "assistant", "system"):
                continue
            msgs.append({"role": role, "content": m.content or ""})
        msgs.append({"role": "user", "content": msg.text or ""})

        # Call LLM (this also records token usage).
        # If the call fails, we still commit a session with a placeholder reply
        # so the admin dashboard always reflects the channel traffic.
        from datetime import datetime, timezone
        from ...token_usage import record_usage
        try:
            res = chat_for_org(
                db,
                org_id,
                msgs,
                temperature=0.4,
                max_tokens=1024,
                session_id=sess.id,
                message_id=user_msg.id,
            )
            reply = res.content or ""
            asst = Message(
                session_id=sess.id, role="assistant", content=reply,
                tokens_in=res.prompt_tokens, tokens_out=res.completion_tokens,
            )
            db.add(asst)
            # Record usage in the same session —no lock, single commit.
            try:
                record_usage(
                    db,
                    org_id=org_id,
                    model=res.raw.get("model") if isinstance(res.raw, dict) else "",
                    prompt_tokens=res.prompt_tokens,
                    completion_tokens=res.completion_tokens,
                    user_id=None,
                    session_id=sess.id,
                    message_id=asst.id,
                )
            except Exception as ee:
                logger.warning("record_usage on success failed: %s", ee)
        except Exception as e:
            logger.warning("channel LLM call failed: %s", e)
            reply = "(assistant unavailable)"
            asst = Message(
                session_id=sess.id, role="assistant", content=reply,
                tokens_in=0, tokens_out=0,
            )
            db.add(asst)
            try:
                db.flush()
                # We don't know the model here without re-querying; record with the configured endpoint.
                from ...models import LLMEndpoint
                ep = (
                    db.query(LLMEndpoint)
                    .filter(LLMEndpoint.org_id == org_id, LLMEndpoint.enabled == True)  # noqa: E712
                    .order_by(LLMEndpoint.is_default.desc(), LLMEndpoint.created_at.asc())
                    .first()
                )
                model_name = ep.model if ep else "unknown"
                record_usage(
                    db,
                    org_id=org_id,
                    model=model_name,
                    prompt_tokens=0,
                    completion_tokens=0,
                    user_id=None,
                    session_id=sess.id,
                    message_id=asst.id,
                )
            except Exception as ee:
                logger.warning("record_usage on failure failed: %s", ee)
        sess.last_message_at = datetime.now(timezone.utc).replace(tzinfo=None)
        db.commit()

        # Update account last_seen
        try:
            acc = db.get(ChannelAccount, adapter.account_id)
            if acc is not None:
                acc.last_seen_at = datetime.now(timezone.utc).replace(tzinfo=None)
                db.commit()
        except Exception:
            pass

    return OutgoingMessage(kind=msg.kind, external_chat_id=msg.external_chat_id, text=reply)


def _get_system_user_id(db, org_id: str) -> str:
    """Return a user id to attribute channel-initiated sessions to.

    v1: uses the first admin in the org. v2: introduces a per-org bot user.
    """
    from ...models import Membership, User
    m = (
        db.query(Membership)
        .filter(Membership.org_id == org_id, Membership.role.in_(["admin", "owner"]))
        .order_by(Membership.created_at.asc())
        .first()
    )
    if m is not None:
        return m.user_id
    u = db.query(User).order_by(User.created_at.asc()).first()
    if u is not None:
        return u.id
    # Last resort: create one
    u = User(username=f"channel-bot-{org_id[:8]}", password_hash="!")
    db.add(u); db.flush()
    return u.id


def start_all() -> int:
    """Start adapters for all enabled accounts. Returns number started."""
    with _LOCK:
        started = 0
        accounts = _load_accounts()
        for acc in accounts:
            key = f"{acc.kind}:{acc.id}"
            if key in _RUNNING:
                continue
            if acc.kind not in CHANNEL_KINDS:
                logger.warning("unknown channel kind %s for account %s; skipping", acc.kind, acc.id)
                continue
            creds = _decrypt_credentials(acc.credentials_enc)
            try:
                cfg = json.loads(acc.config_json or "{}") if acc.config_json else {}
            except Exception:
                cfg = {}
            cfg.update(creds)
            adapter = build_adapter(
                acc.kind,
                account_id=acc.id,
                org_id=acc.org_id,
                name=acc.name,
                config=cfg,
            )
            adapter.bind(_handle_incoming)
            try:
                adapter.start()
            except Exception as e:
                logger.warning("failed to start channel %s/%s: %s", acc.kind, acc.name, e)
                continue
            _RUNNING[key] = adapter
            started += 1
        if started:
            logger.info("channel manager started %d adapter(s)", started)
        return started


def reload() -> int:
    stop_all()
    return start_all()


def stop_all() -> None:
    with _LOCK:
        for key, adapter in list(_RUNNING.items()):
            try:
                adapter.stop()
            except Exception as e:
                logger.warning("error stopping channel %s: %s", key, e)
        _RUNNING.clear()


def running_keys() -> List[str]:
    with _LOCK:
        return list(_RUNNING.keys())


def _dispatch_to_handler(msg: IncomingMessage) -> Optional[OutgoingMessage]:
    """Public entry point for the webhook router: same code path as the
    in-process polling loop. Returns the OutgoingMessage produced by the
    handler (or None when the message was not routable).
    """
    return _handle_incoming(msg)


__all__ = ["start_all", "stop_all", "reload", "running_keys", "_dispatch_to_handler"]
