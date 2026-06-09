#!/usr/bin/env python
"""End-to-end smoke test for GE-paw."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("GEPAW_BASE", "http://127.0.0.1:8765").rstrip("/") + "/api"


def call(method, path, body=None, token=None, raw=None, content_type=None):
    headers = {}
    if token:
        headers["Authorization"] = "Bearer " + token
    if raw is not None:
        headers["Content-Type"] = content_type or "application/octet-stream"
        data = raw
    elif body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    else:
        data = None
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
    code, body = call("GET", "/health")
    assert code == 200 and body.get("ok"), f"health failed: {code} {body}"
    code, body = call("POST", "/auth/login", {"username": "admin", "password": "admin123"})
    assert code == 200, f"login failed: {code} {body}"
    tok = body["access_token"]
    print("[ok] login")
    code, body = call("POST", "/admin/llm", {
        "name": "smoke", "base_url": "http://127.0.0.1:9/v1", "api_key": "sk-smoke",
        "model": "gpt-4o-mini", "max_tokens": 64, "temperature": 0.0, "is_default": True,
    }, token=tok)
    assert code in (201, 409), f"add LLM failed: {code} {body}"
    print(f"[ok] add LLM: {code}")
    for kind, path in (("skill", "/admin/skills"), ("mcp", "/admin/mcp"), ("plugin", "/admin/plugins")):
        code, body = call("POST", path, {"name": "smoke-" + kind, "manifest": {}}, token=tok)
        assert code in (201, 409), f"add {kind} failed: {code} {body}"
    print("[ok] add skill/mcp/plugin")
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    md = b"# Smoke Test\n\nThis is a smoke test source for GE-paw wiki pipeline."
    parts = [
        ("--" + boundary).encode(),
        ("Content-Disposition: form-data; name=\"file\"; filename=\"smoke.md\"").encode(),
        b"Content-Type: text/markdown",
        b"",
        md,
        ("--" + boundary + "--").encode(),
        b"",
    ]
    body_bytes = b"\r\n".join(parts)
    r = urllib.request.Request(BASE + "/admin/wiki/sources/upload",
                              data=body_bytes,
                              headers={"Content-Type": "multipart/form-data; boundary=" + boundary,
                                       "Authorization": "Bearer " + tok},
                              method="POST")
    try:
        with urllib.request.urlopen(r) as resp:
            src = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"[fail] upload: {e.code} {e.read()[:200]}")
        return 1
    print(f"[ok] upload: {src.get('path')}")
    code, body = call("POST", "/admin/wiki/ingest", {}, token=tok)
    assert code == 200, f"ingest failed: {code} {body}"
    assert body.get("succeeded", 0) >= 1, f"ingest did not succeed: {body}"
    print(f"[ok] ingest: {body}")
    code, body = call("POST", "/admin/wiki/compile", {}, token=tok)
    assert code == 200, f"compile failed: {code} {body}"
    print(f"[ok] compile: {body}")
    code, body = call("POST", "/admin/wiki/lint", {}, token=tok)
    assert code == 200, f"lint failed: {code} {body}"
    print(f"[ok] lint: {body}")
    code, body = call("GET", "/client/wiki/tree?path=wiki", token=tok)
    assert code == 200, f"wiki tree failed: {code} {body}"
    print(f"[ok] wiki tree: {len(body.get('items', []))} items")
    code, body = call("GET", "/client/wiki/tree?path=wiki/raw", token=tok)
    assert code == 403, f"raw should be 403: {code} {body}"
    print("[ok] raw sandbox -> 403")
    code, body = call("GET", "/client/wiki/preview?path=wiki/../etc/passwd", token=tok)
    assert code == 403, f"traversal should be 403: {code} {body}"
    print("[ok] traversal sandbox -> 403")
    code, body = call("POST", "/client/wiki/query", {"question": "smoke"}, token=tok)
    if code == 200:
        print(f"[ok] wiki query: answer len={len(body.get('answer', ''))}, citations={len(body.get('citations', []))}")
    else:
        print(f"[warn] wiki query {code} (real LLM unreachable?): {(body.get('message') if isinstance(body, dict) else str(body))[:120]}")
    print("\nALL SMOKE STEPS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
