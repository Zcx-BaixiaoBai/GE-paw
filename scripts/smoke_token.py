#!/usr/bin/env python
"""End-to-end smoke: chat -> token_usage_log -> admin/tokens/summary.

Run after smoke.py so admin/org/user exist. The LLM endpoint in smoke is
intentionally unreachable, so we expect stub mode and a row with model='stub'.
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

    # Create a chat session and post a message
    code, body = call("POST", "/client/sessions", {"title": "token-smoke"}, token=tok)
    assert code == 201, f"create session: {code} {body}"
    session_id = body["id"]

    code, body = call("POST", f"/client/sessions/{session_id}/messages",
                       {"role": "user", "content": "hello"}, token=tok)
    assert code == 201, f"send user msg: {code} {body}"

    code, body = call("POST", "/client/chat", {"session_id": session_id, "message": "ping"}, token=tok)
    # 200 ok (stub gives a reply) or 500 (real LLM unreachable) both should produce a usage row
    # In stub mode, chat_for_org is called, so usage should be recorded even on real failure path
    print("chat ->", code, str(body)[:200])

    # Check tokens/summary (admin) — must show at least 1 call attributed to admin user
    code, summary = call("GET", "/admin/tokens/summary", token=tok)
    assert code == 200, f"tokens/summary: {code} {summary}"
    print("tokens/summary ->", summary)
    assert summary.get("calls", 0) >= 1, "expected at least 1 token usage row"

    # by_user
    code, by_user = call("GET", "/admin/tokens/by_user", token=tok)
    assert code == 200, f"by_user: {code} {by_user}"
    print("by_user ->", by_user)
    assert by_user["items"], "expected by_user items"

    # month_to_date
    code, mtd = call("GET", "/admin/tokens/month_to_date", token=tok)
    assert code == 200, f"month_to_date: {code} {mtd}"
    print("month_to_date ->", mtd)
    assert mtd["calls"] >= 1

    # cost_table
    code, ct = call("GET", "/admin/tokens/cost_table", token=tok)
    assert code == 200, f"cost_table: {code} {ct}"
    assert "gpt-4o" in ct["known_models"]
    # Set an override
    code, _ = call("PUT", "/admin/tokens/cost_table/test-model-xyz",
                    {"prompt_cents_per_1k": 10, "completion_cents_per_1k": 20}, token=tok)
    assert code == 200
    code, ct2 = call("GET", "/admin/tokens/cost_table", token=tok)
    assert "test-model-xyz" in ct2["overrides"]
    code, _ = call("DELETE", "/admin/tokens/cost_table/test-model-xyz", token=tok)
    assert code == 204
    print("cost_table override roundtrip -> ok")

    print("ALL TOKEN SMOKE STEPS PASSED")


if __name__ == "__main__":
    sys.exit(main() or 0)
