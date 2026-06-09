"""Client API extensions for right-side tabs (Diff / Preview / Plan).

These endpoints back the placeholder DiffTab / PreviewTab / PlanTab
components. v1 keeps them minimal: every endpoint returns a stable JSON
shape so the tabs can be wired up now, and richer data can be plugged in
later without changing the frontend contract.
"""
from __future__ import annotations

import difflib
import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ...constant import WIKI_FILE_MAX_BYTES, WIKI_PREVIEW_MAX_BYTES
from ...models import ChatSession, Message, WikiCorpus
from ...utils.logging import get_logger
from ...wiki.store import get_wiki_store
from ..db import get_db
from ..deps import Principal, require_user

logger = get_logger("routers.client_extras")
extras_router = APIRouter(prefix="/api/client", tags=["client-extras"])


def _resolve_corpus(db: Session, org_id: str) -> WikiCorpus:
    corpus = db.query(WikiCorpus).filter(WikiCorpus.org_id == org_id).first()
    if corpus is None:
        from ...constant import WIKI_ROOT
        corpus = WikiCorpus(
            org_id=org_id,
            name="default",
            root_path=str(WIKI_ROOT / org_id / "wiki"),
            storage_kind="fs",
        )
        db.add(corpus)
        db.commit()
        db.refresh(corpus)
    return corpus


def _safe_wiki_subpath(path: str) -> str:
    p = (path or "").replace("\\", "/").strip("/")
    if not p:
        return "wiki"
    parts: List[str] = []
    for seg in p.split("/"):
        if seg in ("", "."):
            continue
        if seg == "..":
            raise PermissionError("path out of range")
        parts.append(seg)
    if not parts or parts[0] != "wiki":
        parts = ["wiki", *parts]
    rel = "/".join(parts)
    if rel == "wiki/raw" or rel.startswith("wiki/raw/"):
        raise PermissionError("raw sources are not exposed to clients")
    if rel == "wiki/graph" or rel.startswith("wiki/graph/"):
        raise PermissionError("graph data is not exposed to clients")
    return rel


@extras_router.get("/diff")
def diff(
    left: str = Query(..., max_length=500),
    right: str = Query(..., max_length=500),
    principal: Principal = Depends(require_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Return a unified diff between two wiki pages (for DiffTab)."""
    left_rel = _safe_wiki_subpath(left)
    right_rel = _safe_wiki_subpath(right)
    corpus = _resolve_corpus(db, principal.org.id)
    store = get_wiki_store(corpus)
    try:
        left_text = store.read_text(left_rel, max_bytes=WIKI_FILE_MAX_BYTES)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"left not found: {left_rel}")
    except ValueError as e:
        raise HTTPException(status_code=413, detail=str(e))
    try:
        right_text = store.read_text(right_rel, max_bytes=WIKI_FILE_MAX_BYTES)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"right not found: {right_rel}")
    except ValueError as e:
        raise HTTPException(status_code=413, detail=str(e))
    left_lines = left_text.splitlines(keepends=True)
    right_lines = right_text.splitlines(keepends=True)
    diff_iter = difflib.unified_diff(left_lines, right_lines, fromfile=left_rel, tofile=right_rel, n=3)
    diff_text = "".join(diff_iter)
    matcher = difflib.SequenceMatcher(a=left_text, b=right_text, autojunk=False)
    ratio = matcher.ratio()
    return {
        "left": left_rel,
        "right": right_rel,
        "ratio": round(ratio, 4),
        "diff": diff_text,
        "left_size": len(left_text),
        "right_size": len(right_text),
    }


@extras_router.get("/plan")
def plan(
    session_id: str = Query(..., max_length=64),
    principal: Principal = Depends(require_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Return the latest assistant turn's tool_calls as a plan list.

    Falls back to an empty plan (frontend renders the placeholder).
    """
    sess = db.get(ChatSession, session_id)
    if sess is None or sess.org_id != principal.org.id or sess.user_id != principal.user.id:
        raise HTTPException(status_code=404, detail="session not found")
    rows = (
        db.query(Message)
        .filter(Message.session_id == session_id, Message.role == "assistant")
        .order_by(Message.created_at.desc())
        .limit(20)
        .all()
    )
    plan_steps: List[Dict[str, Any]] = []
    for m in rows:
        if not m.tool_calls_json:
            continue
        try:
            calls = json.loads(m.tool_calls_json)
        except Exception:
            continue
        if not isinstance(calls, list):
            continue
        for c in calls:
            if not isinstance(c, dict):
                continue
            plan_steps.append({
                "message_id": m.id,
                "tool": c.get("name") or c.get("tool") or "tool",
                "args": c.get("arguments") or c.get("args") or c.get("input") or {},
                "status": c.get("status") or "called",
                "at": m.created_at.isoformat() if m.created_at else None,
            })
    plan_steps.reverse()
    return {
        "session_id": session_id,
        "steps": plan_steps,
        "status": "ok" if plan_steps else "empty",
        "hint": "Assistant plan tool calls appear here once the agent records them." if not plan_steps else None,
    }


@extras_router.get("/preview-data")
def preview_data(
    path: str = Query(..., max_length=500),
    principal: Principal = Depends(require_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Tab-friendly preview payload (metadata + safe content) for PreviewTab.

    Frontend PreviewTab uses this to render multi-format previews without
    having to re-implement markdown / bleach on the client. The iframe-based
    /api/client/wiki/preview is also kept; PreviewTab can switch between them.
    """
    rel = _safe_wiki_subpath(path)
    if not rel.startswith("wiki"):
        raise HTTPException(status_code=403, detail="only wiki subtree is accessible")
    corpus = _resolve_corpus(db, principal.org.id)
    store = get_wiki_store(corpus)
    try:
        body = store.read_text(rel, max_bytes=WIKI_PREVIEW_MAX_BYTES)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=413, detail=str(e))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="file not found")
    headline = ""
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("#"):
            headline = s.lstrip("#").strip()
            break
    words = re.findall(r"\w+", body)
    return {
        "path": rel,
        "size": len(body),
        "lines": body.count("\n") + 1,
        "words": len(words),
        "headline": headline or "(untitled)",
        "preview_url": "/api/client/wiki/preview?path=" + rel,
        "file_url": "/api/client/wiki/file?path=" + rel,
        "snippet": body[:1200],
    }


__all__ = ["extras_router"]
