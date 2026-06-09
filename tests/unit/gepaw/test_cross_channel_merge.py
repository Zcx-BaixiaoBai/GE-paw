"""Unit tests for Org.cross_channel_merge routing strategy.

We mock chat_for_org so the test does not need a real LLM, then drive the
manager._handle_incoming code path directly. Two ChannelAccount rows
representing two different IM kinds (both using EchoAdapter under the hood)
deliver an IncomingMessage with the same external_chat_id. Depending on the
org's cross_channel_merge flag, the routing must either keep the two
sessions isolated or merge them into a single session whose
channel_kind/channel_account_id fields track the most recent source.
"""
from __future__ import annotations

import pytest

import json
import os
import sys
import tempfile
from datetime import datetime

pytestmark = pytest.mark.skip(reason="cross-channel merge dispatch not yet implemented")


def _isolated_env():
    tmp = tempfile.mkdtemp(prefix="gepaw-ccm-")
    os.environ["GEPAW_SECRET_KEY"] = "test-secret-key-32-bytes-padding-padding-pad"
    os.environ["GEPAW_DATA_DIR"] = tmp
    os.environ["GEPAW_DATABASE_URL"] = f"sqlite:///{tmp}/test.db"
    os.environ["GEPAW_DOCS"] = "0"
    for mod in [m for m in list(sys.modules) if m.startswith("gepaw")]:
        del sys.modules[mod]


def _bootstrap_org_with_two_accounts(org_merge: bool):
    """Create one Org, two ChannelAccounts (telegram + feishu), return (org_id, acc_tg, acc_fs)."""
    from gepaw.app.db import init_db, session_scope
    from gepaw.models import Org, ChannelAccount
    from gepaw.security.crypto import encrypt

    init_db()
    with session_scope() as db:
        org = Org(name="TestOrg", slug=f"t-{os.urandom(2).hex()}", cross_channel_merge=org_merge)
        db.add(org); db.flush()
        org_id = org.id

        creds = encrypt(json.dumps({"token": "stub"}))
        acc_tg = ChannelAccount(
            org_id=org_id, kind="telegram", name="tg", enabled=True,
            config_json=json.dumps({}), credentials_enc=creds,
        )
        acc_fs = ChannelAccount(
            org_id=org_id, kind="feishu", name="fs", enabled=True,
            config_json=json.dumps({}), credentials_enc=creds,
        )
        db.add(acc_tg); db.add(acc_fs); db.flush()
        return org_id, acc_tg.id, acc_fs.id


def _install_running_adapter(manager, account_id: str, org_id: str, kind: str):
    """Build a real EchoAdapter and register it in the manager so the handler can find it."""
    from gepaw.app.channels.kinds.echo import EchoAdapter
    adapter = EchoAdapter(account_id=account_id, org_id=org_id, name=f"{kind}-{account_id[:4]}", config={})
    adapter._handler = manager._handle_incoming
    manager._RUNNING[f"{kind}:{account_id}"] = adapter
    return adapter


class _StubResult:
    def __init__(self, content: str = "ok"):
        self.content = content
        self.prompt_tokens = 5
        self.completion_tokens = 3
        self.total_tokens = 8
        self.raw = {"model": "stub-model"}


def _send(manager, kind, account_id, chat_id, text):
    """Build an IncomingMessage with the right account_id stamp and dispatch it."""
    from gepaw.app.channels.base import IncomingMessage
    m = IncomingMessage(kind=kind, external_user_id="u1", external_chat_id=chat_id, text=text)
    m.raw = {"account_id": account_id}
    return manager._handle_incoming(m)


def test_cross_channel_isolated_by_default():
    """Org.cross_channel_merge = False: same external_chat_id from two kinds -> two sessions."""
    _isolated_env()
    from gepaw.app.channels import manager as channel_manager
    from gepaw.app.db import session_scope
    from gepaw.models import ChatSession
    from gepaw.wiki import llm_client as llm_client_mod

    def fake_chat_for_org(db, org_id, messages, **kwargs):
        return _StubResult("hello")
    llm_client_mod.chat_for_org = fake_chat_for_org
    channel_manager.chat_for_org = fake_chat_for_org

    org_id, acc_tg, acc_fs = _bootstrap_org_with_two_accounts(org_merge=False)
    _install_running_adapter(channel_manager, acc_tg, org_id, "telegram")
    _install_running_adapter(channel_manager, acc_fs, org_id, "feishu")

    try:
        _send(channel_manager, "telegram", acc_tg, "chat-9", "hi from tg")
        _send(channel_manager, "feishu", acc_fs, "chat-9", "hi from fs")

        with session_scope() as db:
            sessions = (
                db.query(ChatSession)
                .filter(ChatSession.org_id == org_id, ChatSession.title == "#chat-9")
                .order_by(ChatSession.created_at.asc())
                .all()
            )
        assert len(sessions) == 2, f"isolated mode should create 2 sessions, got {len(sessions)}"
        kinds = {s.channel_kind for s in sessions}
        assert kinds == {"telegram", "feishu"}, kinds
    finally:
        channel_manager.stop_all()


def test_cross_channel_merge_unifies_sessions():
    """Org.cross_channel_merge = True: same external_chat_id from two kinds -> one session; channel_kind updates to latest source."""
    _isolated_env()
    from gepaw.app.channels import manager as channel_manager
    from gepaw.app.db import session_scope
    from gepaw.models import ChatSession, Message
    from gepaw.wiki import llm_client as llm_client_mod

    def fake_chat_for_org(db, org_id, messages, **kwargs):
        return _StubResult("merged-reply")
    llm_client_mod.chat_for_org = fake_chat_for_org
    channel_manager.chat_for_org = fake_chat_for_org

    org_id, acc_tg, acc_fs = _bootstrap_org_with_two_accounts(org_merge=True)
    _install_running_adapter(channel_manager, acc_tg, org_id, "telegram")
    _install_running_adapter(channel_manager, acc_fs, org_id, "feishu")

    try:
        _send(channel_manager, "telegram", acc_tg, "chat-M", "first")
        _send(channel_manager, "feishu", acc_fs, "chat-M", "second")

        with session_scope() as db:
            sessions = (
                db.query(ChatSession)
                .filter(ChatSession.org_id == org_id, ChatSession.title == "#chat-M")
                .all()
            )
        assert len(sessions) == 1, f"merge mode should keep 1 session, got {len(sessions)}"
        sess = sessions[0]
        # channel_kind is updated to the most recent source
        assert sess.channel_kind == "feishu", f"expected feishu (latest), got {sess.channel_kind}"
        assert sess.channel_account_id == acc_fs
        # Both user messages should be persisted under the same session id
        with session_scope() as db:
            msgs = (
                db.query(Message)
                .filter(Message.session_id == sess.id, Message.role == "user")
                .order_by(Message.created_at.asc())
                .all()
            )
        texts = [m.content for m in msgs]
        assert texts == ["first", "second"], texts
    finally:
        channel_manager.stop_all()
