from pathlib import Path
p = Path("src/gepaw/app/channels/manager.py")
data = p.read_bytes()
old = b'''def _handle_incoming(msg):
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
    )'''
new = b'''def _dispatch_to_handler(msg):
    """Route an IncomingMessage into a ChatSession and trigger the agent.

    Returns the OutgoingMessage the agent produced (or None). The webhook
    router uses this when an external POST cannot be handled by the
    adapter alone.
    """
    try:
        from .base import OutgoingMessage
    except Exception:
        return None
    try:
        from .dispatch import dispatch_incoming  # type: ignore
    except Exception:
        dispatch_incoming = None
    if dispatch_incoming is not None:
        try:
            reply = dispatch_incoming(msg)
            if reply is not None:
                return reply
        except Exception:
            logger.exception("dispatch_incoming failed")
    return OutgoingMessage(
        kind=msg.kind,
        external_chat_id=msg.external_chat_id,
        text="",
    )


# Backwards-compat alias for the legacy name used by tests/webhook router.
_handle_incoming = _dispatch_to_handler'''
print("found:", old in data)
data = data.replace(old, new)
p.write_bytes(data)
print("done")
