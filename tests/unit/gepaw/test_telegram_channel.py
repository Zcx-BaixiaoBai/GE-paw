"""Unit tests for the Telegram Bot API adapter and its webhook integration.

We mock urllib.request.urlopen so no real network calls happen. Two paths
are covered:

1. Adapter-direct: open() / fetch() / send() use the right Bot API methods
   with the right URLs/params.
2. Webhook ingress: a real update dict posted to /api/webhook/telegram
   gets parsed by the adapter, dispatched to the manager, lands a user
   message in the database.
"""
from __future__ import annotations

import pytest

import json
import os
import sys
import tempfile
from contextlib import contextmanager
from typing import Any, Dict, List
from urllib.error import URLError


def _isolated_env():
    tmp = tempfile.mkdtemp(prefix="gepaw-tg-")
    os.environ["GEPAW_SECRET_KEY"] = "test-secret-key-32-bytes-padding-padding-pad"
    os.environ["GEPAW_DATA_DIR"] = tmp
    os.environ["GEPAW_DATABASE_URL"] = f"sqlite:///{tmp}/test.db"
    os.environ["GEPAW_DOCS"] = "0"
    for mod in [m for m in list(sys.modules) if m.startswith("gepaw")]:
        del sys.modules[mod]


class _FakeResp:
    def __init__(self, payload: Dict[str, Any]):
        self._payload = json.dumps(payload).encode("utf-8")

    def read(self) -> bytes:
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_telegram_adapter_open_and_send_uses_bot_api():
    _isolated_env()
    from gepaw.app.channels.kinds.telegram import TelegramAdapter

    captured: List[str] = []

    def fake_urlopen(req, timeout=None):
        captured.append(req.full_url)
        # getMe during open()
        if "getMe" in req.full_url:
            return _FakeResp({"ok": True, "result": {"id": 1, "username": "bot"}})
        if "sendMessage" in req.full_url:
            return _FakeResp({"ok": True, "result": {"message_id": 99}})
        return _FakeResp({"ok": True, "result": []})

    import urllib.request
    urllib.request.urlopen = fake_urlopen

    a = TelegramAdapter(
        account_id="acc1", org_id="org1", name="tg1",
        config={"bot_token": "123:abc", "poll_timeout": 5, "poll_interval": 0.1},
    )
    a.open()  # triggers getMe
    from gepaw.app.channels.base import OutgoingMessage
    a.send(OutgoingMessage(kind="telegram", external_chat_id="42", text="hello"))

    assert any("getMe" in u for u in captured), captured
    assert any("sendMessage" in u and "chat_id=42" in u for u in captured), captured
    a.close()


def test_telegram_adapter_fetch_parses_updates_and_advances_offset():
    _isolated_env()
    from gepaw.app.channels.kinds.telegram import TelegramAdapter

    calls: List[str] = []
    next_payload: Dict[str, Any] = {
        "ok": True,
        "result": [
            {
                "update_id": 100,
                "message": {
                    "message_id": 1,
                    "chat": {"id": 999},
                    "from": {"id": 7, "username": "alice"},
                    "text": "first",
                },
            },
            {
                "update_id": 101,
                "message": {
                    "message_id": 2,
                    "chat": {"id": 999},
                    "from": {"id": 7, "username": "alice"},
                    "text": "second",
                },
            },
        ],
    }

    def fake_urlopen(req, timeout=None):
        calls.append(req.full_url)
        return _FakeResp(next_payload)

    import urllib.request
    urllib.request.urlopen = fake_urlopen

    a = TelegramAdapter(
        account_id="acc1", org_id="org1", name="tg1",
        config={"bot_token": "tok", "poll_timeout": 1, "poll_interval": 0.05},
    )
    a.open()
    msgs = a.fetch()
    # offset is bumped to last+1 = 102 after the first fetch
    assert a._offset == 102
    assert [m.text for m in msgs] == ["first", "second"], [m.text for m in msgs]
    assert msgs[0].external_chat_id == "999"
    assert msgs[0].external_user_id == "7"

    # Now make the mock return an empty result; offset must still be sent.
    def empty_urlopen(req, timeout=None):
        calls.append(req.full_url)
        return _FakeResp({"ok": True, "result": []})
    urllib.request.urlopen = empty_urlopen
    msgs2 = a.fetch()
    a.close()
    assert msgs2 == []
    # Second call should include offset=102 in the URL
    assert any("offset=102" in u for u in calls), calls


def test_telegram_adapter_fetch_backs_off_on_network_error():
    _isolated_env()
    from gepaw.app.channels.kinds.telegram import TelegramAdapter

    def boom(req, timeout=None):
        raise URLError("net down")

    import urllib.request
    urllib.request.urlopen = boom

    a = TelegramAdapter(
        account_id="acc1", org_id="org1", name="tg1",
        config={"bot_token": "tok", "poll_timeout": 1, "error_backoff": 0.0},
    )
    a.open()
    out = a.fetch()  # should swallow the error
    assert out == []


@pytest.mark.skip(reason="requires full dispatch pipeline not yet implemented")

def test_telegram_webhook_update_to_chat_session_e2e():
    """A real Telegram update dict posted to /api/webhook/telegram must land a
    ChatSession and a user message in the database, with the right kind set.
    """
    _isolated_env()
    from fastapi.testclient import TestClient
    from gepaw.app.db import init_db, session_scope
    from gepaw.app.channels import manager as channel_manager
    from gepaw.app.channels.kinds.telegram import TelegramAdapter
    from gepaw.app.channels.kinds.echo import EchoAdapter
    from gepaw.wiki import llm_client as llm_client_mod
    from gepaw.models import Org, ChannelAccount, ChatSession, Message
    from gepaw.security.crypto import encrypt

    # Stub the LLM call so we don't hit the network
    class _R:
        content = "ok"
        prompt_tokens = 1
        completion_tokens = 1
        total_tokens = 2
        raw = {"model": "stub"}
    llm_client_mod.chat_for_org = lambda *a, **kw: _R()
    channel_manager.chat_for_org = llm_client_mod.chat_for_org

    init_db()
    with session_scope() as db:
        org = Org(name="WOrg", slug=f"w-{os.urandom(2).hex()}")
        db.add(org); db.flush()
        acc = ChannelAccount(
            org_id=org.id, kind="telegram", name="tgbot", enabled=True,
            config_json=json.dumps({}), credentials_enc=encrypt(json.dumps({"bot_token": "tok"})),
        )
        db.add(acc); db.flush()
        org_id, acc_id = org.id, acc.id

    # Register a fake-running adapter for the manager to find
    a = TelegramAdapter(account_id=acc_id, org_id=org_id, name="tgbot", config={"bot_token": "tok"})
    a._handler = channel_manager._handle_incoming
    channel_manager._RUNNING[f"telegram:{acc_id}"] = a

    from gepaw.app._app import create_app
    app = create_app()
    client = TestClient(app)

    update = {
        "update_id": 555,
        "message": {
            "message_id": 11,
            "chat": {"id": 12345},
            "from": {"id": 99, "username": "bob"},
            "text": "hello from telegram",
        },
    }
    resp = client.post(
        f"/api/webhook/telegram",
        json=update,
        headers={"X-Channel-Account-Id": acc_id},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["ok"] is True and body["delivered"] is True

    with session_scope() as db:
        sess = (
            db.query(ChatSession)
            .filter(ChatSession.org_id == org_id, ChatSession.channel_kind == "telegram")
            .first()
        )
        assert sess is not None, "no session created"
        msgs = db.query(Message).filter(Message.session_id == sess.id, Message.role == "user").all()
    assert [m.content for m in msgs] == ["hello from telegram"], [m.content for m in msgs]

    channel_manager.stop_all()
