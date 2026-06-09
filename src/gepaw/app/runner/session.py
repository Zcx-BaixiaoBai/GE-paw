"""Crash-resilient JSON session store.

``SafeJSONSession`` mirrors the subset of the ``agentscope.session.SessionBase``
contract used by gepaw / QwenPaw, but reads the on-disk JSON with a lenient
strategy so a partially-written or otherwise corrupt file does not take down
an agent. Writes always go out as strict, re-encoded JSON, so the next read
is fast and clean.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

# Reserved characters in user / session ids that are rewritten in filenames.
_FILENAME_SAFE_RE = re.compile(r"[^A-Za-z0-9_-]+")


class SafeJSONSession:
    """Per-session JSON store that tolerates corrupt / partial files.

    Files are stored under ``save_dir`` as ``<user_id>_<session_id>.json``
    with a single JSON object as content. ``:`` in the session id is
    rewritten to ``--`` (e.g. ``"test:session"`` -> ``"test--session.json"``).
    """

    def __init__(self, save_dir):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def _safe_name(self, value):
        return _FILENAME_SAFE_RE.sub("--", value or "").strip("-_") or "_"

    def _get_save_path(self, user_id, session_id):
        parts = [self._safe_name(user_id), self._safe_name(session_id)]
        if not parts[0] or parts[0] == "_":
            return self.save_dir / (parts[1] + ".json")
        return self.save_dir / (parts[0] + "_" + parts[1] + ".json")

    @staticmethod
    def _decode_lenient(raw_bytes):
        if not raw_bytes:
            return {}
        try:
            text = raw_bytes.decode("utf-8", errors="replace")
        except Exception:
            return {}
        text = text.strip()
        if not text:
            return {}
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            value = None
        if isinstance(value, dict):
            return value
        decoder = json.JSONDecoder()
        for idx, ch in enumerate(text):
            if ch not in "{[":
                continue
            try:
                obj, _end = decoder.raw_decode(text[idx:])
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                return obj
        return {}

    def _read_state(self, session_id, user_id):
        path = self._get_save_path(user_id, session_id)
        try:
            raw = path.read_bytes()
        except (FileNotFoundError, OSError):
            return {}
        return self._decode_lenient(raw)

    def _write_state(self, session_id, user_id, state):
        path = self._get_save_path(user_id, session_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(state, ensure_ascii=False, sort_keys=True)
        path.write_text(payload, encoding="utf-8")

    @staticmethod
    def _ensure_path(root, parts):
        cur = root
        for part in parts[:-1]:
            nxt = cur.get(part)
            if not isinstance(nxt, dict):
                nxt = {}
                cur[part] = nxt
            cur = nxt
        return cur

    @staticmethod
    def _set_dotted(root, key, value):
        parts = [p for p in key.split(".") if p]
        if not parts:
            return
        target = SafeJSONSession._ensure_path(root, parts)
        target[parts[-1]] = value

    async def load_session_state(
        self,
        session_id,
        user_id="",
        allow_not_exist=True,
        **state_modules,
    ):
        state = self._read_state(session_id, user_id)
        if not state and not allow_not_exist:
            return
        for key, module in state_modules.items():
            if not hasattr(module, "load_state_dict"):
                continue
            module.load_state_dict(state.get(key))

    async def get_session_state_dict(
        self,
        session_id,
        user_id="",
        allow_not_exist=True,
    ):
        state = self._read_state(session_id, user_id)
        if not state and not allow_not_exist:
            return {}
        return state

    async def update_session_state(
        self,
        session_id,
        key,
        value,
        user_id="",
        channel="",
    ):
        del channel
        state = self._read_state(session_id, user_id)
        self._set_dotted(state, key, value)
        self._write_state(session_id, user_id, state)