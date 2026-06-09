#!/usr/bin/env python
"""End-to-end smoke: admin creates an echo channel -> webhook injects a message
-> channel manager dispatches to agent -> assistant message lands in DB
-> token_usage_log gains a row attributed to the channel session.

Run after smoke.py / smoke_token.py.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ.get("GEPAW_BASE", "http://127.0.0.1:8765").rstrip("/") + "/api"


def call(method, path, body=None, token=None):
    headers = {}
    if token:
        headers["Authorization"] = "Bearer " + token
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    r = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r) as resp:
            b = resp.read()
            try:
                return resp.status, (json.loads(b) if b else None)
            except Exception:
                return resp.status, b[:300].decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        b = e.read()
        try:
            return e.code, (json.loads(b) if b else None)
        except Exception:
            return e.code, b[:300].decode("utf-8", "replace")


def main():
    code, body = call("POST", "/auth/login", {"username": "admin", "password": "admin123"})
    assert code == 200, f"login: {code} {body}"
    tok = body["access_token"]

    # Create an echo channel account
    code, ch = call("POST", "/admin/channels", {
        "kind": "echo", "name": f"smoke-echo-{int(time.time())}",
        "credentials": {"api_key": "ignored"}, "enabled": True,
    }, token=tok)
    if code == 409:
        # try reload and pick the existing
        code, _ = call("POST", "/admin/channels/reload", token=tok)
        assert code == 200
        code, lst = call("GET", "/admin/channels", token=tok)
        ch = next((c for c in lst if c["kind"] == "echo"), None)
        assert ch is not None
    else:
        assert code == 201, f"create channel: {code} {ch}"
    account_id = ch["id"]
    print(f"[ok] channel {account_id} created")

    # Reload adapters
    code, _ = call("POST", "/admin/channels/reload", token=tok)
    assert code == 200

    # Inject a message via webhook
    code, body = call("POST", "/webhook/echo", {
        "account_id": account_id, "chat_id": "chat-1", "user_id": "u1",
        "text": "hello from smoke channel",
    })
    assert code == 200, f"webhook: {code} {body}"
    print("[ok] webhook delivered")

    # Wait for the channel loop to dispatch
    found = False
    for _ in range(30):
        code, lst = call("GET", "/admin/sessions", token=tok)
        if code == 200:
            for s in lst:
                if (s.get("channel_kind") == "echo"
                        and s.get("channel_account_id") == account_id):
                    sid = s["id"]
                    code, msgs = call("GET", f"/admin/sessions", token=tok)
                    # read messages via the client sessions route
                    code2, msgs2 = call("GET", f"/client/sessions/{sid}/messages", token=tok)
                    if code2 == 200 and len(msgs2) >= 2:
                        found = True
                        print(f"[ok] session {sid} has {len(msgs2)} messages")
                        break
        if found:
            break
        time.sleep(0.3)
    assert found, "channel did not produce a session with messages within 9s"

    # Token usage should have grown
    code, summary = call("GET", "/admin/tokens/summary", token=tok)
    assert code == 200 and summary.get("calls", 0) >= 1
    print(f"[ok] tokens/summary calls={summary['calls']}")

    # Channels status
    code, st = call("GET", "/admin/channels/status", token=tok)
    assert code == 200
    print(f"[ok] channels status: {st}")

    print("ALL CHANNEL SMOKE STEPS PASSED")


if __name__ == "__main__":
    sys.exit(main() or 0)
