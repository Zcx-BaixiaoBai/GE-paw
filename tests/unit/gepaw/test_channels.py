"""Unit tests for the channel adapter system."""
from __future__ import annotations

import os
import sys
import tempfile
import time


def _isolated_env() -> str:
    from conftest import _isolated_env as _cf_isolated_env
    return _cf_isolated_env("gepaw-ch")

def test_registry_known_kinds():
    _isolated_env()
    from gepaw.app.channels.registry import CHANNEL_KINDS, build_adapter, get_adapter_class
    assert "echo" in CHANNEL_KINDS
    assert "telegram" in CHANNEL_KINDS
    # Build an echo adapter
    a = build_adapter("echo", account_id="acc1", org_id="org1", name="test", config={})
    assert a.kind == "echo"
    assert a.org_id == "org1"
    # Fallback for unsupported kind still returns a usable adapter
    b = build_adapter("telegram", account_id="acc2", org_id="org1", name="tg", config={})
    assert b.org_id == "org1"


def test_echo_adapter_dispatch():
    _isolated_env()
    from gepaw.app.channels import manager as channel_manager
    from gepaw.app.channels.base import IncomingMessage, OutgoingMessage
    from gepaw.app.channels.kinds.echo import EchoAdapter

    received = []

    def handler(msg: IncomingMessage) -> OutgoingMessage:
        return OutgoingMessage(kind=msg.kind, external_chat_id=msg.external_chat_id, text="echo: " + msg.text)

    a = EchoAdapter(account_id="acc1", org_id="org1", name="e1", config={"poll_interval": 0.1})
    a.bind(handler)
    a.start()
    try:
        a.deliver(IncomingMessage(kind="echo", external_user_id="u1", external_chat_id="c1", text="hi"))
        # Poll a few times until the sent_log shows the reply
        for _ in range(20):
            if a.config.get("sent_log"):
                break
            time.sleep(0.1)
        log = a.config.get("sent_log") or []
        assert any(item["text"].startswith("echo: hi") for item in log), f"no echo reply: {log}"
    finally:
        a.stop()


def test_manager_start_all_with_no_accounts():
    _isolated_env()
    from gepaw.app.channels import manager as channel_manager
    from gepaw.app.db import init_db
    init_db()
    n = channel_manager.start_all()
    assert n == 0
    assert channel_manager.running_keys() == []
    channel_manager.stop_all()
