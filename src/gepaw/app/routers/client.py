"""Client-facing API (authenticated, user-scoped)."""
from __future__ import annotations

import bleach
import json
import markdown as md_lib
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse, StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ...constant import WIKI_FILE_MAX_BYTES, WIKI_PREVIEW_MAX_BYTES
from ...models import (
    ChatSession, LLMEndpoint, MCPServer, Message, Plugin, Skill, WikiCorpus,
)
from ...utils.logging import get_logger
from ...wiki.llm_client import chat_for_org
from ...wiki.pipeline import run_query
from ...wiki.store import get_wiki_store
from ..db import get_db
from ..deps import Principal, require_user

logger = get_logger("routers.client")
client_router = APIRouter(prefix="/api/client", tags=["client"])

ALLOWED_TAGS = [
    "a", "p", "span", "div", "h1", "h2", "h3", "h4", "h5", "h6",
    "ul", "ol", "li", "blockquote", "pre", "code", "em", "strong",
    "hr", "br", "table", "thead", "tbody", "tr", "th", "td", "img",
]
ALLOWED_ATTRS = {
    "a": ["href", "title", "rel", "target"],
    "img": ["src", "alt", "title"],
    "code": ["class"],
    "span": ["class"],
    "div": ["class"],
}


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


def _safe_subpath(path: str) -> str:
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
    # Explicit deny: clients must not see raw/ or graph/ subtrees
    if rel == "wiki/raw" or rel.startswith("wiki/raw/"):
        raise PermissionError("raw sources are not exposed to clients")
    if rel == "wiki/graph" or rel.startswith("wiki/graph/"):
        raise PermissionError("graph data is not exposed to clients")
    return rel


@client_router.get("/config")
def get_config(principal: Principal = Depends(require_user), db: Session = Depends(get_db)) -> Dict[str, Any]:
    ep: Optional[LLMEndpoint] = (
        db.query(LLMEndpoint)
        .filter(LLMEndpoint.org_id == principal.org.id, LLMEndpoint.enabled == True)  # noqa: E712
        .order_by(LLMEndpoint.is_default.desc(), LLMEndpoint.created_at.asc())
        .first()
    )
    skills = db.query(Skill).filter(Skill.org_id == principal.org.id, Skill.enabled == True).all()  # noqa: E712
    mcps = db.query(MCPServer).filter(MCPServer.org_id == principal.org.id, MCPServer.enabled == True).all()  # noqa: E712
    plugins = db.query(Plugin).filter(Plugin.org_id == principal.org.id, Plugin.enabled == True).all()  # noqa: E712
    return {
        "org": {"id": principal.org.id, "name": principal.org.name, "slug": principal.org.slug},
        "user": {"id": principal.user.id, "username": principal.user.username, "display_name": principal.user.display_name, "role": principal.role},
        "llm": (
            {"id": ep.id, "name": ep.name, "base_url": ep.base_url, "model": ep.model, "max_tokens": ep.max_tokens, "temperature": ep.temperature}
            if ep else None
        ),
        "skills": [{"id": s.id, "name": s.name} for s in skills],
        "mcp": [{"id": m.id, "name": m.name, "transport": m.transport} for m in mcps],
        "plugins": [{"id": p.id, "name": p.name} for p in plugins],
        "wiki_path": "wiki",
    }


class SessionIn(BaseModel):
    title: str = Field(default="New session", max_length=200)


@client_router.get("/sessions")
def list_sessions(principal: Principal = Depends(require_user), db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    rows = (
        db.query(ChatSession)
        .filter(ChatSession.org_id == principal.org.id, ChatSession.user_id == principal.user.id, ChatSession.archived == False)  # noqa: E712
        .order_by(ChatSession.last_message_at.desc().nullslast(), ChatSession.created_at.desc())
        .limit(200)
        .all()
    )
    return [
        {
            "id": s.id, "title": s.title, "status": s.status, "pinned": s.pinned,
            "channel_kind": s.channel_kind,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "last_message_at": s.last_message_at.isoformat() if s.last_message_at else None,
        }
        for s in rows
    ]


@client_router.post("/sessions", status_code=201)
def create_session(payload: SessionIn, principal: Principal = Depends(require_user), db: Session = Depends(get_db)) -> Dict[str, Any]:
    s = ChatSession(org_id=principal.org.id, user_id=principal.user.id, title=payload.title or "New session")
    db.add(s); db.commit(); db.refresh(s)
    return {"id": s.id, "title": s.title, "status": s.status, "created_at": s.created_at.isoformat()}


@client_router.get("/sessions/{session_id}/messages")
def list_messages(session_id: str, principal: Principal = Depends(require_user), db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    s = db.get(ChatSession, session_id)
    if s is None or s.org_id != principal.org.id or s.user_id != principal.user.id:
        raise HTTPException(status_code=404, detail="session not found")
    rows = db.query(Message).filter(Message.session_id == s.id).order_by(Message.created_at.asc()).all()
    return [
        {
            "id": m.id, "role": m.role, "content": m.content,
            "tool_calls": json.loads(m.tool_calls_json) if m.tool_calls_json else None,
            "tokens_in": m.tokens_in, "tokens_out": m.tokens_out,
            "created_at": m.created_at.isoformat(),
        }
        for m in rows
    ]


class MessageIn(BaseModel):
    content: str = Field(min_length=1, max_length=20000)


@client_router.post("/sessions/{session_id}/messages", status_code=201)
def append_message(session_id: str, payload: MessageIn, principal: Principal = Depends(require_user), db: Session = Depends(get_db)) -> Dict[str, Any]:
    s = db.get(ChatSession, session_id)
    if s is None or s.org_id != principal.org.id or s.user_id != principal.user.id:
        raise HTTPException(status_code=404, detail="session not found")
    m = Message(session_id=s.id, role="user", content=payload.content)
    db.add(m); s.last_message_at = m.created_at
    db.commit(); db.refresh(m)
    return {"id": m.id, "role": m.role, "content": m.content, "created_at": m.created_at.isoformat()}


class ChatIn(BaseModel):
    session_id: Optional[str] = None
    message: str = Field(min_length=1, max_length=20000)


@client_router.post("/chat")
def chat(payload: ChatIn, principal: Principal = Depends(require_user), db: Session = Depends(get_db)) -> Dict[str, Any]:
    s = _ensure_session(db, principal, payload.session_id)
    import time
    t0 = time.time()
    msgs = _build_history(db, s.id, with_user=payload.message)
    user_msg = Message(session_id=s.id, role="user", content=payload.message)
    db.add(user_msg); s.last_message_at = user_msg.created_at
    try:
        res = chat_for_org(
            db,
            principal.org.id,
            msgs,
            temperature=0.4,
            max_tokens=2048,
            user_id=principal.user.id,
            session_id=s.id,
        )
        asst = Message(
            session_id=s.id, role="assistant", content=res.content or "",
            tokens_in=res.prompt_tokens, tokens_out=res.completion_tokens,
            latency_ms=int((time.time() - t0) * 1000),
        )
    except Exception as e:
        logger.warning("chat LLM call failed, recording stub usage: %s", e)
        from ...token_usage import record_usage as _record_usage
        _record_usage(
            db,
            org_id=principal.org.id,
            model="(unreachable)",
            prompt_tokens=0,
            completion_tokens=0,
            user_id=principal.user.id,
            session_id=s.id,
            commit=True,
        )
        asst = Message(
            session_id=s.id, role="assistant",
            content="(assistant unavailable: " + str(e)[:300] + ")",
            tokens_in=0, tokens_out=0,
            latency_ms=int((time.time() - t0) * 1000),
        )
    db.add(asst)
    if s.title in ("", "New session"):
        s.title = (payload.message[:40] + "...") if len(payload.message) > 40 else payload.message
    db.commit()
    return {"session_id": s.id, "reply": asst.content, "tokens_in": asst.tokens_in, "tokens_out": asst.tokens_out}


@client_router.post("/chat/stream")
def chat_stream(payload: ChatIn, principal: Principal = Depends(require_user), db: Session = Depends(get_db)) -> StreamingResponse:
    s = _ensure_session(db, principal, payload.session_id)
    msgs = _build_history(db, s.id, with_user=payload.message)
    return StreamingResponse(
        _sse_chat(db, principal, s, msgs, payload.message),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"},
    )


def _ensure_session(db: Session, principal: Principal, session_id: Optional[str]) -> ChatSession:
    if session_id:
        s = db.get(ChatSession, session_id)
        if s is None or s.org_id != principal.org.id or s.user_id != principal.user.id:
            raise HTTPException(status_code=404, detail="session not found")
        return s
    s = ChatSession(org_id=principal.org.id, user_id=principal.user.id, title="New session")
    db.add(s); db.commit(); db.refresh(s)
    return s


def _build_history(db: Session, session_id: str, with_user: str) -> List[Dict[str, str]]:
    rows = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at.asc()).all()
    out = [{"role": "system", "content": "You are GE-paw assistant. Be concise and helpful."}]
    for r in rows:
        if r.content:
            out.append({"role": r.role, "content": r.content})
    out.append({"role": "user", "content": with_user})
    return out


async def _sse_chat(db: Session, principal: Principal, s: ChatSession, msgs: List[Dict[str, str]], user_text: str):
    import time
    t0 = time.time()
    full = ""
    try:
        for chunk in _chat_stream_iter(db, principal.org.id, msgs):
            full += chunk
            yield f"event: delta\ndata: {json.dumps({'text': chunk}, ensure_ascii=False)}\n\n"
    except Exception as e:
        logger.warning("chat stream LLM failed, recording stub usage: %s", e)
        try:
            from ...token_usage import record_usage as _record_usage
            _record_usage(
                db,
                org_id=principal.org.id,
                model="(unreachable)",
                prompt_tokens=0,
                completion_tokens=0,
                user_id=principal.user.id,
                session_id=s.id,
                commit=True,
            )
        except Exception:
            pass
        yield f"event: error\ndata: {json.dumps({'message': str(e)[:300]})}\n\n"
        return
    user_msg = Message(session_id=s.id, role="user", content=user_text)
    asst = Message(session_id=s.id, role="assistant", content=full, latency_ms=int((time.time() - t0) * 1000))
    db.add_all([user_msg, asst]); s.last_message_at = asst.created_at
    if s.title in ("", "New session"):
        s.title = (user_text[:40] + "...") if len(user_text) > 40 else user_text
    db.commit()
    yield f"event: done\ndata: {json.dumps({'session_id': s.id, 'reply': full[:200]})}\n\n"


def _chat_stream_iter(db: Session, org_id: str, msgs: List[Dict[str, str]]):
    # Single non-streaming call; we chunk the result into deltas to simulate
    # streaming over SSE. chat_for_org has already recorded token usage.
    res = chat_for_org(
        db,
        org_id,
        msgs,
        temperature=0.4,
        max_tokens=2048,
    )
    if isinstance(res, dict) and "content" in res:
        text = res["content"] or ""
    else:
        text = str(getattr(res, "content", "") or "")
    # Chunk into ~40-char slices for a smooth SSE delta stream
    CHUNK = 40
    for i in range(0, len(text), CHUNK):
        yield text[i:i + CHUNK]


@client_router.get("/wiki/tree")
def wiki_tree(path: str = Query(default="wiki", max_length=500), principal: Principal = Depends(require_user), db: Session = Depends(get_db)) -> Dict[str, Any]:
    rel = _safe_subpath(path)
    if not rel.startswith("wiki"):
        raise HTTPException(status_code=403, detail="only wiki subtree is accessible")
    corpus = _resolve_corpus(db, principal.org.id)
    store = get_wiki_store(corpus)
    nodes = store.list_tree(sub="wiki", max_depth=8)
    if rel != "wiki":
        nodes = [n for n in nodes if n.path == rel or n.path.startswith(rel + "/")]
    return {
        "corpus_id": corpus.id,
        "root": "wiki",
        "items": [
            {"name": n.name, "path": n.path, "type": n.type, "size": n.size, "mtime": n.mtime}
            for n in nodes
        ],
    }


@client_router.get("/wiki/file", response_class=PlainTextResponse)
def wiki_file(path: str = Query(..., max_length=500), principal: Principal = Depends(require_user), db: Session = Depends(get_db)) -> str:
    rel = _safe_subpath(path)
    if not rel.startswith("wiki"):
        raise HTTPException(status_code=403, detail="only wiki subtree is accessible")
    corpus = _resolve_corpus(db, principal.org.id)
    store = get_wiki_store(corpus)
    try:
        return store.read_text(rel, max_bytes=WIKI_FILE_MAX_BYTES)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=413, detail=f"file too large; use preview. ({e})")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="file not found")


@client_router.get("/wiki/preview", response_class=PlainTextResponse)
def wiki_preview(path: str = Query(..., max_length=500), principal: Principal = Depends(require_user), db: Session = Depends(get_db)) -> str:
    rel = _safe_subpath(path)
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
    html = md_lib.markdown(body, extensions=["fenced_code", "tables", "toc"])
    safe = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<link rel='stylesheet' href='/static/wiki-preview.css'>"
        "</head><body class='gepaw-wiki'>" + safe + "</body></html>"
    )


class QueryIn(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    top_k: int = Field(default=5, ge=1, le=20)


@client_router.post("/wiki/query")
def wiki_query(payload: QueryIn, principal: Principal = Depends(require_user), db: Session = Depends(get_db)) -> Dict[str, Any]:
    corpus = _resolve_corpus(db, principal.org.id)
    return run_query(corpus, db, question=payload.question, user_id=principal.user.id, top_k=payload.top_k)


_ROOT = Path(os.environ.get("GEPAW_FS_ROOT", "./workspace")).resolve()
_ROOT.mkdir(parents=True, exist_ok=True)


@client_router.get("/fs/list")
def fs_list(path: str = Query(default="."), principal: Principal = Depends(require_user)) -> Dict[str, Any]:
    rel = (path or ".").replace("\\", "/").strip("/")
    if rel in ("", "."):
        target = _ROOT
    else:
        target = (_ROOT / rel).resolve()
    if not str(target).startswith(str(_ROOT)):
        raise HTTPException(status_code=403, detail="path out of sandbox")
    if not target.exists():
        raise HTTPException(status_code=404, detail="path not found")
    items = []
    for p in sorted(target.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
        items.append({
            "name": p.name,
            "type": "dir" if p.is_dir() else "file",
            "size": p.stat().st_size if p.is_file() else 0,
        })
    return {
        "root": str(_ROOT),
        "path": str(target.relative_to(_ROOT)).replace("\\", "/"),
        "items": items,
    }
