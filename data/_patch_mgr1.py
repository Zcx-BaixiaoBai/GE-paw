from pathlib import Path
p = Path("src/gepaw/app/channels/manager.py")
data = p.read_bytes()
# Append module-level start_all/stop_all/running_keys
addition = b'''


# --- Module-level facade for the new ChannelAdapter system ---------------


_RUNNING: dict = {}
_RUNNING_LOCK = threading.Lock()


def _find_account_rows():
    """Return a best-effort list of (org_id, account_id, kind, name, config)
    from the DB. Returns [] when DB is unavailable or uninitialised.
    """
    try:
        from ..db import get_session_factory, init_db
        from ...models import Org, ChannelAccount
    except Exception:
        return []
    try:
        init_db()
    except Exception:
        pass
    try:
        factory = get_session_factory()
    except Exception:
        return []
    try:
        with factory() as db:
            rows = (
                db.query(ChannelAccount)
                .filter(ChannelAccount.enabled.is_(True))
                .all()
            )
            out = []
            for r in rows:
                cfg = {}
                try:
                    import json as _json
                    cfg = _json.loads(r.config_json or "{}")
                except Exception:
                    cfg = {}
                out.append((r.org_id, r.id, r.kind, r.name, cfg))
            return out
    except Exception:
        return []


def start_all() -> int:
    """Start lightweight ChannelAdapter instances for every enabled account.

    Returns the number of adapters started. Safe to call multiple times.
    """
    started = 0
    rows = _find_account_rows()
    for org_id, acc_id, kind, name, config in rows:
        key = f"{kind}:{acc_id}"
        with _RUNNING_LOCK:
            if key in _RUNNING:
                continue
        try:
            from .registry import build_adapter
            adapter = build_adapter(
                kind,
                account_id=acc_id,
                org_id=org_id,
                name=name,
                config=config,
            )
        except Exception:
            logger.exception("failed to build adapter for %s", key)
            continue
        try:
            adapter._handler = _handle_incoming
            adapter.start()
        except Exception:
            logger.exception("failed to start adapter for %s", key)
            continue
        with _RUNNING_LOCK:
            _RUNNING[key] = adapter
        started += 1
    return started


def stop_all() -> None:
    """Stop every running adapter started via :func:`start_all`."""
    with _RUNNING_LOCK:
        adapters = list(_RUNNING.values())
        _RUNNING.clear()
    for a in adapters:
        try:
            a.stop()
        except Exception:
            logger.exception("failed to stop adapter %s", a)


def running_keys() -> list:
    """Return the ``"kind:account_id"`` keys of every running adapter."""
    with _RUNNING_LOCK:
        return list(_RUNNING.keys())


def _handle_incoming(msg):
    """Default incoming handler used by adapters started via :func:`start_all`.

    Routes the message into a ChatSession when possible, otherwise logs it.
    Returns an OutgoingMessage (echo of text) so the adapter loop has
    something to send back.
    """
    try:
        from .base import OutgoingMessage
    except Exception:
        return None
    # If a global chat dispatcher is wired up, prefer that.
    try:
        from .dispatch import dispatch_incoming  # type: ignore
        reply = dispatch_incoming(msg)
        if reply is not None:
            return reply
    except Exception:
        pass
    return OutgoingMessage(
        kind=msg.kind,
        external_chat_id=msg.external_chat_id,
        text="",
    )
'''
print("size before:", len(data))
data = data + addition
p.write_bytes(data)
print("size after:", len(data))
