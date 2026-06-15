"""管理后台路由（合并：orgs/users/llm/skills/mcp/plugins/channels/crons/tokens/sessions/wiki/audit）。"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from croniter import croniter
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ...constant import WIKI_FILE_MAX_BYTES, WIKI_PREVIEW_MAX_BYTES, WIKI_ROOT
from ..audit import write_audit
from ...models import (
    AuditLog, ChannelAccount, ChatSession, CronJob, CronRun, LLMEndpoint,
    MCPServer, Membership, Message, Org, Plugin, Skill, TokenUsageLog, User,
    WikiCorpus, WikiSource,
)
from ...security.crypto import encrypt
from ...security.passwords import hash_password
from ...utils.logging import get_logger
from ...wiki.pipeline import run_compile, run_ingest, run_lint
from ...wiki.store import get_wiki_store
from ..db import get_db
from ..deps import Principal, require_admin

logger = get_logger("routers.admin")
admin_router = APIRouter(prefix="/api/admin", tags=["admin"])

_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,58}[a-z0-9]$")
from ..channels.registry import CHANNEL_KINDS  # noqa: F401


# ---------- orgs / users ----------

@admin_router.get("/orgs")
def list_orgs(principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    rows = db.query(Org).order_by(Org.created_at.asc()).all()
    return [{"id": o.id, "name": o.name, "slug": o.slug, "cross_channel_merge": o.cross_channel_merge} for o in rows]


class OrgIn(BaseModel):
    name: str
    slug: str = Field(min_length=3, max_length=60)


@admin_router.post("/orgs", status_code=201)
def create_org(payload: OrgIn, principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> Dict[str, Any]:
    if not _SLUG_RE.match(payload.slug):
        raise HTTPException(status_code=400, detail="slug 不合法")
    org = Org(name=payload.name, slug=payload.slug)
    db.add(org)
    try: db.commit()
    except IntegrityError:
        db.rollback(); raise HTTPException(status_code=409, detail="slug 已存在")
    write_audit(db, action="org.create", actor_id=principal.user.id, org_id=org.id, target=org.id)
    db.commit()
    return {"id": org.id, "name": org.name, "slug": org.slug, "cross_channel_merge": org.cross_channel_merge}


@admin_router.patch("/orgs/{org_id}")
def update_org(org_id: str, payload: Dict[str, Any], principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> Dict[str, Any]:
    o: Optional[Org] = db.get(Org, org_id)
    if o is None: raise HTTPException(status_code=404, detail="组织不存在")
    if "name" in payload: o.name = str(payload["name"])[:120]
    if "cross_channel_merge" in payload: o.cross_channel_merge = bool(payload["cross_channel_merge"])
    db.commit()
    write_audit(db, action="org.update", actor_id=principal.user.id, org_id=o.id, target=o.id, detail=payload)
    db.commit()
    return {"id": o.id, "name": o.name, "slug": o.slug, "cross_channel_merge": o.cross_channel_merge}


@admin_router.delete("/orgs/{org_id}", status_code=204)
def delete_org(org_id: str, principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> None:
    o: Optional[Org] = db.get(Org, org_id)
    if o is None: raise HTTPException(status_code=404, detail="组织不存在")
    db.delete(o); db.commit()
    write_audit(db, action="org.delete", actor_id=principal.user.id, org_id=org_id, target=org_id)


@admin_router.get("/users")
def list_users(principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    rows = db.query(User).order_by(User.created_at.asc()).all()
    out = []
    for u in rows:
        out.append({
            "id": u.id, "username": u.username, "display_name": u.display_name, "email": u.email,
            "is_super_admin": u.is_super_admin, "is_active": u.is_active,
            "memberships": [{"org_id": m.org_id, "role": m.role, "org_name": m.org.name} for m in u.memberships],
        })
    return out


class UserIn(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=8, max_length=200)
    display_name: Optional[str] = None
    email: Optional[str] = None
    is_super_admin: bool = False
    org_roles: List[Dict[str, str]] = []


@admin_router.post("/users", status_code=201)
def create_user(payload: UserIn, principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> Dict[str, Any]:
    u = User(
        username=payload.username, display_name=payload.display_name, email=payload.email,
        password_hash=hash_password(payload.password), is_super_admin=payload.is_super_admin,
    )
    db.add(u)
    try: db.flush()
    except IntegrityError:
        db.rollback(); raise HTTPException(status_code=409, detail="用户名已存在")
    for entry in payload.org_roles:
        oid = entry.get("org_id"); role = entry.get("role", "user")
        if not oid or db.get(Org, oid) is None: continue
        db.add(Membership(user_id=u.id, org_id=oid, role=role))
    db.commit()
    write_audit(db, action="user.create", actor_id=principal.user.id, target=u.id, detail={"username": u.username})
    db.commit()
    return {
        "id": u.id, "username": u.username, "display_name": u.display_name, "email": u.email,
        "is_super_admin": u.is_super_admin, "is_active": u.is_active,
        "memberships": [{"org_id": m.org_id, "role": m.role, "org_name": m.org.name} for m in u.memberships],
    }


@admin_router.patch("/users/{user_id}")
def update_user(user_id: str, payload: Dict[str, Any], principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> Dict[str, Any]:
    u: Optional[User] = db.get(User, user_id)
    if u is None: raise HTTPException(status_code=404, detail="用户不存在")
    for f in ("display_name", "email"):
        if f in payload and payload[f] is not None: setattr(u, f, str(payload[f]))
    if "is_active" in payload: u.is_active = bool(payload["is_active"])
    if "is_super_admin" in payload: u.is_super_admin = bool(payload["is_super_admin"])
    if "password" in payload and payload["password"]: u.password_hash = hash_password(str(payload["password"]))
    if "org_roles" in payload:
        db.query(Membership).filter(Membership.user_id == u.id).delete()
        for entry in payload["org_roles"]:
            oid = entry.get("org_id"); role = entry.get("role", "user")
            if not oid or db.get(Org, oid) is None: continue
            db.add(Membership(user_id=u.id, org_id=oid, role=role))
    db.commit()
    write_audit(db, action="user.update", actor_id=principal.user.id, target=u.id, detail=payload)
    db.commit()
    return {
        "id": u.id, "username": u.username, "display_name": u.display_name, "email": u.email,
        "is_super_admin": u.is_super_admin, "is_active": u.is_active,
        "memberships": [{"org_id": m.org_id, "role": m.role, "org_name": m.org.name} for m in u.memberships],
    }


@admin_router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: str, principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> None:
    u: Optional[User] = db.get(User, user_id)
    if u is None: raise HTTPException(status_code=404, detail="用户不存在")
    if u.id == principal.user.id: raise HTTPException(status_code=400, detail="不能删除自己")
    db.delete(u); db.commit()
    write_audit(db, action="user.delete", actor_id=principal.user.id, target=user_id)



# ---------- Channel ----------

class ChannelIn(BaseModel):
    kind: str
    name: str
    credentials: Dict[str, Any] = Field(default_factory=dict)
    config: Optional[Dict[str, Any]] = None
    enabled: bool = True


@admin_router.get("/channels/kinds", response_model=List[str])
def channel_kinds() -> List[str]:
    return CHANNEL_KINDS


@admin_router.get("/channels")
def list_channels(principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    rows = db.query(ChannelAccount).filter(ChannelAccount.org_id == principal.org.id).order_by(ChannelAccount.created_at.asc()).all()
    return [{
        "id": r.id, "kind": r.kind, "name": r.name, "enabled": r.enabled, "status": r.status,
        "last_seen_at": r.last_seen_at.isoformat() if r.last_seen_at else None,
        "has_credentials": bool(r.credentials_enc),
    } for r in rows]


@admin_router.post("/channels", status_code=201)
def create_channel(payload: ChannelIn, principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> Dict[str, Any]:
    if payload.kind not in CHANNEL_KINDS:
        raise HTTPException(status_code=400, detail=f"不支持的 channel kind: {payload.kind}")
    row = ChannelAccount(
        org_id=principal.org.id, kind=payload.kind, name=payload.name,
        credentials_enc=encrypt(json.dumps(payload.credentials, ensure_ascii=False)),
        config_json=json.dumps(payload.config, ensure_ascii=False) if payload.config else None,
        enabled=payload.enabled,
    )
    db.add(row)
    try: db.flush()
    except IntegrityError:
        db.rollback(); raise HTTPException(status_code=409, detail="同kind 下同同channel 已存在")
    db.commit()
    write_audit(db, action="channel.create", actor_id=principal.user.id, org_id=principal.org.id, target=row.id, detail={"kind": row.kind, "name": row.name})
    db.commit()
    return {"id": row.id, "kind": row.kind, "name": row.name, "enabled": row.enabled, "status": row.status, "last_seen_at": None, "has_credentials": True}


@admin_router.patch("/channels/{channel_id}")
def update_channel(channel_id: str, payload: Dict[str, Any], principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> Dict[str, Any]:
    row: Optional[ChannelAccount] = db.query(ChannelAccount).filter(ChannelAccount.id == channel_id, ChannelAccount.org_id == principal.org.id).first()
    if row is None: raise HTTPException(status_code=404, detail="频道不存在")
    if "name" in payload: row.name = str(payload["name"])[:120]
    if "credentials" in payload: row.credentials_enc = encrypt(json.dumps(payload["credentials"], ensure_ascii=False))
    if "config" in payload: row.config_json = json.dumps(payload["config"], ensure_ascii=False) if payload["config"] else None
    if "enabled" in payload: row.enabled = bool(payload["enabled"])
    db.commit()
    write_audit(db, action="channel.update", actor_id=principal.user.id, org_id=principal.org.id, target=row.id, detail=payload)
    db.commit()
    return {"id": row.id, "kind": row.kind, "name": row.name, "enabled": row.enabled, "status": row.status, "last_seen_at": row.last_seen_at.isoformat() if row.last_seen_at else None, "has_credentials": bool(row.credentials_enc)}


@admin_router.delete("/channels/{channel_id}", status_code=204)
def delete_channel(channel_id: str, principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> None:
    row: Optional[ChannelAccount] = db.query(ChannelAccount).filter(ChannelAccount.id == channel_id, ChannelAccount.org_id == principal.org.id).first()
    if row is None: raise HTTPException(status_code=404, detail="频道不存在")
    db.delete(row); db.commit()
    write_audit(db, action="channel.delete", actor_id=principal.user.id, org_id=principal.org.id, target=channel_id)


# ---------- Cron ----------

class CronIn(BaseModel):
    name: str
    schedule_cron: str
    prompt_template: str
    target_session_id: Optional[str] = None
    target_channel_account_id: Optional[str] = None
    enabled: bool = True


def _next_run(expr: str) -> Optional[datetime]:
    try: return croniter(expr, datetime.now(timezone.utc).replace(tzinfo=None)).get_next(datetime)
    except Exception: return None


@admin_router.get("/crons")
def list_crons(principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    rows = db.query(CronJob).filter(CronJob.org_id == principal.org.id).order_by(CronJob.created_at.asc()).all()
    return [{
        "id": r.id, "name": r.name, "schedule_cron": r.schedule_cron, "prompt_template": r.prompt_template,
        "target_session_id": r.target_session_id, "target_channel_account_id": r.target_channel_account_id,
        "enabled": r.enabled, "failure_count": r.failure_count, "last_status": r.last_status,
        "last_run_at": r.last_run_at.isoformat() if r.last_run_at else None,
        "next_run_at": _next_run(r.schedule_cron).isoformat() if r.schedule_cron and r.enabled else None,
    } for r in rows]


@admin_router.post("/crons", status_code=201)
def create_cron(payload: CronIn, principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> Dict[str, Any]:
    if not croniter.is_valid(payload.schedule_cron):
        raise HTTPException(status_code=400, detail="cron 表达式不合法")
    row = CronJob(
        org_id=principal.org.id, name=payload.name, schedule_cron=payload.schedule_cron,
        prompt_template=payload.prompt_template, target_session_id=payload.target_session_id,
        target_channel_account_id=payload.target_channel_account_id, enabled=payload.enabled,
    )
    db.add(row); db.commit()
    write_audit(db, action="cron.create", actor_id=principal.user.id, org_id=principal.org.id, target=row.id)
    db.commit()
    from ...app.scheduler import reload
    reload()
    return {"id": row.id, "name": row.name, "schedule_cron": row.schedule_cron, "prompt_template": row.prompt_template,
        "target_session_id": row.target_session_id, "target_channel_account_id": row.target_channel_account_id,
        "enabled": row.enabled, "failure_count": 0, "last_status": None,
        "last_run_at": None, "next_run_at": _next_run(row.schedule_cron).isoformat() if row.enabled else None}


@admin_router.patch("/crons/{cron_id}")
def update_cron(cron_id: str, payload: Dict[str, Any], principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> Dict[str, Any]:
    row: Optional[CronJob] = db.query(CronJob).filter(CronJob.id == cron_id, CronJob.org_id == principal.org.id).first()
    if row is None: raise HTTPException(status_code=404, detail="cron 不存在")
    if "schedule_cron" in payload and not croniter.is_valid(payload["schedule_cron"]):
        raise HTTPException(status_code=400, detail="cron 表达式不合法")
    for f in ("name", "schedule_cron", "prompt_template", "target_session_id", "target_channel_account_id"):
        if f in payload and payload[f] is not None: setattr(row, f, payload[f])
    if "enabled" in payload: row.enabled = bool(payload["enabled"])
    db.commit()
    write_audit(db, action="cron.update", actor_id=principal.user.id, org_id=principal.org.id, target=row.id, detail=payload)
    db.commit()
    from ...app.scheduler import reload
    reload()
    return {"id": row.id, "name": row.name, "schedule_cron": row.schedule_cron, "prompt_template": row.prompt_template,
        "target_session_id": row.target_session_id, "target_channel_account_id": row.target_channel_account_id,
        "enabled": row.enabled, "failure_count": row.failure_count, "last_status": row.last_status,
        "last_run_at": row.last_run_at.isoformat() if row.last_run_at else None,
        "next_run_at": _next_run(row.schedule_cron).isoformat() if row.enabled else None}


@admin_router.delete("/crons/{cron_id}", status_code=204)
def delete_cron(cron_id: str, principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> None:
    row: Optional[CronJob] = db.query(CronJob).filter(CronJob.id == cron_id, CronJob.org_id == principal.org.id).first()
    if row is None: raise HTTPException(status_code=404, detail="cron 不存在")
    db.delete(row); db.commit()
    write_audit(db, action="cron.delete", actor_id=principal.user.id, org_id=principal.org.id, target=cron_id)
    from ...app.scheduler import reload
    reload()


@admin_router.get("/crons/{cron_id}/runs")
def cron_runs(cron_id: str, limit: int = 20, principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    if db.query(CronJob).filter(CronJob.id == cron_id, CronJob.org_id == principal.org.id).first() is None:
        raise HTTPException(status_code=404, detail="cron 不存在")
    rows = db.query(CronRun).filter(CronRun.cron_id == cron_id).order_by(CronRun.started_at.desc()).limit(limit).all()
    return [{
        "id": r.id, "started_at": r.started_at.isoformat(),
        "finished_at": r.finished_at.isoformat() if r.finished_at else None,
        "status": r.status, "tokens_in": r.tokens_in, "tokens_out": r.tokens_out,
        "output_excerpt": r.output_excerpt, "error": r.error,
    } for r in rows]


# ---------- Token 计量 ----------

@admin_router.get("/tokens/summary")
def tokens_summary(
    from_: Optional[datetime] = Query(default=None, alias="from"),
    to: Optional[datetime] = None,
    principal: Principal = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    if from_ is None: from_ = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=30)
    if to is None: to = datetime.now(timezone.utc).replace(tzinfo=None)
    rows = (
        db.query(
            TokenUsageLog.model,
            func.coalesce(func.sum(TokenUsageLog.prompt_tokens), 0),
            func.coalesce(func.sum(TokenUsageLog.completion_tokens), 0),
            func.coalesce(func.sum(TokenUsageLog.total_tokens), 0),
            func.coalesce(func.sum(TokenUsageLog.cost_cents), 0),
            func.count(TokenUsageLog.id),
        )
        .filter(TokenUsageLog.org_id == principal.org.id, TokenUsageLog.occurred_at >= from_, TokenUsageLog.occurred_at <= to)
        .group_by(TokenUsageLog.model)
        .all()
    )
    by_model = [{"model": m, "prompt_tokens": int(p), "completion_tokens": int(c),
                   "total_tokens": int(t), "cost_cents": int(co), "calls": int(n)} for (m, p, c, t, co, n) in rows]
    return {
        "from": from_.isoformat(), "to": to.isoformat(),
        "by_model": by_model,
        "calls": sum(b["calls"] for b in by_model),
        "total_tokens": sum(b["total_tokens"] for b in by_model),
        "prompt_tokens": sum(b["prompt_tokens"] for b in by_model),
        "completion_tokens": sum(b["completion_tokens"] for b in by_model),
        "cost_cents": sum(b["cost_cents"] for b in by_model),
    }



@admin_router.get("/tokens/by_day")
def tokens_by_day(
    days: int = Query(default=30, ge=1, le=365),
    principal: Principal = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    from ...token_usage import manager as tu_manager
    return {
        "days": days,
        "items": [b.to_dict() for b in tu_manager.by_day(
            db, principal.org.id,
            since=datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=days),
        )],
    }


@admin_router.get("/tokens/by_user")
def tokens_by_user(
    limit: int = Query(default=20, ge=1, le=200),
    principal: Principal = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    from ...token_usage import manager as tu_manager
    return {"items": tu_manager.by_user(db, principal.org.id, limit=limit)}


@admin_router.get("/tokens/month_to_date")
def tokens_month_to_date(
    principal: Principal = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    from ...token_usage import manager as tu_manager
    return tu_manager.month_to_date(db, principal.org.id)


@admin_router.get("/tokens/cost_table")
def get_cost_table(
    principal: Principal = Depends(require_admin),
) -> Dict[str, Any]:
    from ...token_usage import cost_table as ct
    return {
        "overrides": ct.list_overrides(),
        "known_models": ct.known_models(),
    }


@admin_router.put("/tokens/cost_table/{model}")
def put_cost_override(
    model: str,
    payload: Dict[str, Any],
    principal: Principal = Depends(require_admin),
) -> Dict[str, Any]:
    from ...token_usage import cost_table as ct
    p = int(payload.get("prompt_cents_per_1k", 0))
    c = int(payload.get("completion_cents_per_1k", 0))
    ct.set_override(model, p, c)
    return {"model": model, "prompt_cents_per_1k": p, "completion_cents_per_1k": c}


@admin_router.delete("/tokens/cost_table/{model}", status_code=204)
def del_cost_override(
    model: str,
    principal: Principal = Depends(require_admin),
) -> None:
    from ...token_usage import cost_table as ct
    ct.clear_override(model)



# ---------- 会话管理 ----------

@admin_router.get("/sessions")
def list_sessions(
    q: Optional[str] = None, user_id: Optional[str] = None, channel_kind: Optional[str] = None,
    limit: int = 50, principal: Principal = Depends(require_admin), db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    qry = db.query(ChatSession, User).join(User, User.id == ChatSession.user_id).filter(ChatSession.org_id == principal.org.id)
    if user_id: qry = qry.filter(ChatSession.user_id == user_id)
    if channel_kind: qry = qry.filter(ChatSession.channel_kind == channel_kind)
    if q: qry = qry.filter(ChatSession.title.contains(q))
    rows = qry.order_by(ChatSession.last_message_at.desc(), ChatSession.created_at.desc()).limit(limit).all()
    out = []
    for s, u in rows:
        count = db.query(func.count(Message.id)).filter(Message.session_id == s.id).scalar() or 0
        out.append({
            "id": s.id, "user_id": u.id, "username": u.username, "title": s.title, "channel_kind": s.channel_kind, "channel_account_id": s.channel_account_id,
            "status": s.status, "pinned": s.pinned, "archived": s.archived,
            "created_at": s.created_at.isoformat(),
            "last_message_at": s.last_message_at.isoformat() if s.last_message_at else None,
            "message_count": int(count),
        })
    return out


@admin_router.delete("/sessions/{session_id}", status_code=204)
def delete_session(session_id: str, principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> None:
    s: Optional[ChatSession] = db.query(ChatSession).filter(ChatSession.id == session_id, ChatSession.org_id == principal.org.id).first()
    if s is None: raise HTTPException(status_code=404, detail="会话不存在")
    db.delete(s); db.commit()
    write_audit(db, action="session.delete", actor_id=principal.user.id, org_id=principal.org.id, target=session_id)


@admin_router.post("/sessions/{session_id}/archive")
def archive_session(session_id: str, principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> Dict[str, Any]:
    s: Optional[ChatSession] = db.query(ChatSession).filter(ChatSession.id == session_id, ChatSession.org_id == principal.org.id).first()
    if s is None: raise HTTPException(status_code=404, detail="会话不存在")
    s.archived = not s.archived
    db.commit()
    write_audit(db, action="session.archive" if s.archived else "session.unarchive", actor_id=principal.user.id, org_id=principal.org.id, target=session_id)
    db.commit()
    u = db.get(User, s.user_id)
    return {
        "id": s.id, "user_id": s.user_id, "username": u.username if u else "", "title": s.title,
        "channel_kind": s.channel_kind, "status": s.status, "pinned": s.pinned, "archived": s.archived,
        "created_at": s.created_at.isoformat(),
        "last_message_at": s.last_message_at.isoformat() if s.last_message_at else None,
        "message_count": db.query(func.count(Message.id)).filter(Message.session_id == s.id).scalar() or 0,
    }



@admin_router.post("/channels/reload")
def reload_channels(principal: Principal = Depends(require_admin)) -> Dict[str, Any]:
    from ..channels import manager as channel_manager
    n = channel_manager.reload()
    return {"started": n, "running": channel_manager.running_keys()}


@admin_router.get("/channels/status")
def channels_status(principal: Principal = Depends(require_admin)) -> Dict[str, Any]:
    from ..channels import manager as channel_manager
    return {"running": channel_manager.running_keys()}


# ---------- Wiki 管理 ----------

@admin_router.get("/wiki/corpus")
def get_corpus(principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> Dict[str, Any]:
    c: Optional[WikiCorpus] = db.query(WikiCorpus).filter(WikiCorpus.org_id == principal.org.id).first()
    if c is None:
        root = (Path(WIKI_ROOT) / principal.org.id / "wiki").resolve()
        c = WikiCorpus(org_id=principal.org.id, name="default", root_path=str(root), storage_kind="fs")
        db.add(c); db.commit()
    return {"id": c.id, "name": c.name, "root_path": c.root_path, "storage_kind": c.storage_kind}


@admin_router.post("/wiki/corpus/reset")
def reset_corpus(principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> Dict[str, Any]:
    c: Optional[WikiCorpus] = db.query(WikiCorpus).filter(WikiCorpus.org_id == principal.org.id).first()
    if c is None: raise HTTPException(status_code=404, detail="语料不存在")
    store = get_wiki_store(c)
    store.purge()
    db.query(WikiSource).filter(WikiSource.corpus_id == c.id).delete()
    db.commit()
    write_audit(db, action="wiki.reset", actor_id=principal.user.id, org_id=principal.org.id, target=c.id)
    db.commit()
    return {"id": c.id, "name": c.name, "root_path": c.root_path, "storage_kind": c.storage_kind}


@admin_router.get("/wiki/sources")
def list_sources(principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    c = db.query(WikiCorpus).filter(WikiCorpus.org_id == principal.org.id).first()
    if c is None: return []
    rows = db.query(WikiSource).filter(WikiSource.corpus_id == c.id).order_by(WikiSource.created_at.desc()).limit(200).all()
    return [{
        "id": s.id, "sha256": s.sha256, "path": s.path, "size_bytes": s.size_bytes, "mime": s.mime,
        "title": s.title, "status": s.status,
        "last_ingested_at": s.last_ingested_at.isoformat() if s.last_ingested_at else None,
        "error": s.error,
    } for s in rows]


@admin_router.post("/wiki/sources/upload", status_code=201)
async def upload_source(
    file: UploadFile = File(...), title: Optional[str] = Form(default=None),
    principal: Principal = Depends(require_admin), db: Session = Depends(get_db),
) -> Dict[str, Any]:
    c = db.query(WikiCorpus).filter(WikiCorpus.org_id == principal.org.id).first()
    if c is None:
        root = (Path(WIKI_ROOT) / principal.org.id / "wiki").resolve()
        c = WikiCorpus(org_id=principal.org.id, name="default", root_path=str(root), storage_kind="fs")
        db.add(c); db.commit()
    data = await file.read()
    if not data: raise HTTPException(status_code=400, detail="空文件")
    sha = hashlib.sha256(data).hexdigest()
    store = get_wiki_store(c)
    rel = store.put_raw(name=file.filename or "untitled", data=data)
    row = WikiSource(corpus_id=c.id, sha256=sha, path=rel, size_bytes=len(data), mime=file.content_type, title=title or file.filename, status="pending")
    db.add(row); db.commit()
    write_audit(db, action="wiki.upload", actor_id=principal.user.id, org_id=principal.org.id, target=row.id, detail={"path": rel, "size": len(data)})
    db.commit()
    return {"id": row.id, "sha256": row.sha256, "path": row.path, "size_bytes": row.size_bytes, "mime": row.mime,
            "title": row.title, "status": row.status, "last_ingested_at": None, "error": None}


@admin_router.post("/wiki/sources/{source_id}/ingest")
def ingest_source(source_id: str, principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> Dict[str, Any]:
    c = db.query(WikiCorpus).filter(WikiCorpus.org_id == principal.org.id).first()
    if c is None: raise HTTPException(status_code=404, detail="语料不存在")
    src: Optional[WikiSource] = db.query(WikiSource).filter(WikiSource.id == source_id, WikiSource.corpus_id == c.id).first()
    if src is None: raise HTTPException(status_code=404, detail="源不存在")
    try: run_ingest(c, src, db)
    except Exception as e:
        src.error = str(e); src.status = "failed"; db.commit()
        raise HTTPException(status_code=500, detail=f"ingest 失败: {e}")
    write_audit(db, action="wiki.ingest", actor_id=principal.user.id, org_id=principal.org.id, target=src.id)
    db.commit()
    return {"id": src.id, "sha256": src.sha256, "path": src.path, "size_bytes": src.size_bytes, "mime": src.mime,
            "title": src.title, "status": src.status, "last_ingested_at": src.last_ingested_at.isoformat() if src.last_ingested_at else None,
            "error": src.error}


@admin_router.post("/wiki/compile")
def compile_corpus(principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> Dict[str, Any]:
    c = db.query(WikiCorpus).filter(WikiCorpus.org_id == principal.org.id).first()
    if c is None: raise HTTPException(status_code=404, detail="语料不存在")
    try: n = run_compile(c, db)
    except Exception as e: raise HTTPException(status_code=500, detail=f"compile 失败: {e}")
    write_audit(db, action="wiki.compile", actor_id=principal.user.id, org_id=principal.org.id, target=c.id)
    db.commit()
    return {"ok": True, "compiled": n}


@admin_router.post("/wiki/lint")
def lint_corpus(principal: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> Dict[str, Any]:
    c = db.query(WikiCorpus).filter(WikiCorpus.org_id == principal.org.id).first()
    if c is None: raise HTTPException(status_code=404, detail="语料不存在")
    res = run_lint(c, db)
    write_audit(db, action="wiki.lint", actor_id=principal.user.id, org_id=principal.org.id, target=c.id)
    db.commit()
    return res


# ---------- Audit ----------

@admin_router.get("/audit")
def list_audit(
    action: Optional[str] = None, actor_id: Optional[str] = None,
    limit: int = 100, offset: int = 0,
    principal: Principal = Depends(require_admin), db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    qry = db.query(AuditLog).filter(AuditLog.org_id == principal.org.id)
    if action: qry = qry.filter(AuditLog.action == action)
    if actor_id: qry = qry.filter(AuditLog.actor_id == actor_id)
    rows = qry.order_by(AuditLog.created_at.desc()).offset(offset).limit(limit).all()
    return [{
        "id": r.id, "action": r.action, "actor_id": r.actor_id, "target": r.target,
        "detail_json": r.detail_json, "ip": r.ip, "created_at": r.created_at.isoformat(),
    } for r in rows]


# ---------- LLM endpoints ----------
class LLMIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    base_url: str = Field(min_length=1, max_length=500)
    api_key: str = ""
    model: str = Field(min_length=1, max_length=200)
    max_tokens: int = 4096
    temperature: float = 0.2
    is_default: bool = False
    enabled: bool = True


def _llm_to_dict(ep):
    return {
        "id": ep.id, "name": ep.name, "base_url": ep.base_url,
        "model": ep.model, "max_tokens": ep.max_tokens, "temperature": ep.temperature,
        "is_default": ep.is_default, "enabled": ep.enabled,
    }


@admin_router.get("/llm")
def list_llm(principal=Depends(require_admin), db=Depends(get_db)):
    rows = (db.query(LLMEndpoint).filter(LLMEndpoint.org_id == principal.org.id)
            .order_by(LLMEndpoint.is_default.desc(), LLMEndpoint.created_at.asc()).all())
    return [_llm_to_dict(r) for r in rows]


@admin_router.post("/llm", status_code=201)
def add_llm(payload: LLMIn, principal=Depends(require_admin), db=Depends(get_db)):
    if payload.is_default:
        db.query(LLMEndpoint).filter(LLMEndpoint.org_id == principal.org.id, LLMEndpoint.is_default == True).update({"is_default": False})  # noqa: E712
    ep = LLMEndpoint(
        org_id=principal.org.id, name=payload.name, base_url=payload.base_url,
        api_key_enc=encrypt(payload.api_key) if payload.api_key else "",
        model=payload.model, max_tokens=payload.max_tokens, temperature=payload.temperature,
        is_default=payload.is_default, enabled=payload.enabled,
    )
    db.add(ep)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="LLM endpoint name already exists")
    db.refresh(ep)
    write_audit(db, action="llm.create", actor_id=principal.user.id, org_id=principal.org.id, target=ep.id)
    db.commit()
    return _llm_to_dict(ep)


@admin_router.delete("/llm/{llm_id}", status_code=204)
def delete_llm(llm_id: str, principal=Depends(require_admin), db=Depends(get_db)):
    ep = db.query(LLMEndpoint).filter(LLMEndpoint.id == llm_id, LLMEndpoint.org_id == principal.org.id).first()
    if ep is None:
        raise HTTPException(status_code=404, detail="not found")
    db.delete(ep)
    write_audit(db, action="llm.delete", actor_id=principal.user.id, org_id=principal.org.id, target=llm_id)
    db.commit()
    return None


# ---------- Skills ----------
class SkillIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    manifest: Dict[str, Any] = {}
    enabled: bool = True


def _skill_to_dict(s):
    try:
        manifest = json.loads(s.manifest_json or "{}")
    except Exception:
        manifest = {}
    return {"id": s.id, "name": s.name, "manifest": manifest, "enabled": s.enabled}


@admin_router.get("/skills")
def list_skills(principal=Depends(require_admin), db=Depends(get_db)):
    rows = db.query(Skill).filter(Skill.org_id == principal.org.id).order_by(Skill.created_at.asc()).all()
    return [_skill_to_dict(r) for r in rows]


@admin_router.post("/skills", status_code=201)
def add_skill(payload: SkillIn, principal=Depends(require_admin), db=Depends(get_db)):
    s = Skill(org_id=principal.org.id, name=payload.name, manifest_json=json.dumps(payload.manifest, ensure_ascii=False), enabled=payload.enabled)
    db.add(s)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="skill name already exists")
    db.refresh(s)
    write_audit(db, action="skill.create", actor_id=principal.user.id, org_id=principal.org.id, target=s.id)
    db.commit()
    return _skill_to_dict(s)


class SkillPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    manifest: dict | None = None
    enabled: bool | None = None


@admin_router.patch("/skills/{skill_id}")
def patch_skill(skill_id: str, payload: SkillPatch, principal=Depends(require_admin), db=Depends(get_db)):
    s = db.query(Skill).filter(Skill.id == skill_id, Skill.org_id == principal.org.id).first()
    if s is None:
        raise HTTPException(status_code=404, detail="not found")
    if payload.name is not None:
        s.name = payload.name
    if payload.manifest is not None:
        s.manifest_json = json.dumps(payload.manifest, ensure_ascii=False)
    if payload.enabled is not None:
        s.enabled = payload.enabled
    write_audit(db, action="skill.patch", actor_id=principal.user.id, org_id=principal.org.id, target=skill_id, detail=payload.model_dump(exclude_none=True))
    db.commit(); db.refresh(s)
    return _skill_to_dict(s)

@admin_router.delete("/skills/{skill_id}", status_code=204)
def delete_skill(skill_id: str, principal=Depends(require_admin), db=Depends(get_db)):
    s = db.query(Skill).filter(Skill.id == skill_id, Skill.org_id == principal.org.id).first()
    if s is None:
        raise HTTPException(status_code=404, detail="not found")
    db.delete(s)
    write_audit(db, action="skill.delete", actor_id=principal.user.id, org_id=principal.org.id, target=skill_id)
    db.commit()
    return None


# ---------- MCP servers ----------
class MCPIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    transport: str = "stdio"
    config: Dict[str, Any] = {}
    enabled: bool = True


def _mcp_to_dict(m):
    try:
        config = json.loads(m.config_json or "{}")
    except Exception:
        config = {}
    return {"id": m.id, "name": m.name, "transport": m.transport, "config": config, "enabled": m.enabled}


@admin_router.get("/mcp")
def list_mcp(principal=Depends(require_admin), db=Depends(get_db)):
    rows = db.query(MCPServer).filter(MCPServer.org_id == principal.org.id).order_by(MCPServer.created_at.asc()).all()
    return [_mcp_to_dict(r) for r in rows]


@admin_router.post("/mcp", status_code=201)
def add_mcp(payload: MCPIn, principal=Depends(require_admin), db=Depends(get_db)):
    m = MCPServer(org_id=principal.org.id, name=payload.name, transport=payload.transport, config_json=json.dumps(payload.config, ensure_ascii=False), enabled=payload.enabled)
    db.add(m)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="mcp name already exists")
    db.refresh(m)
    write_audit(db, action="mcp.create", actor_id=principal.user.id, org_id=principal.org.id, target=m.id)
    db.commit()
    return _mcp_to_dict(m)


class MCPPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    transport: str | None = None
    config: dict | None = None
    enabled: bool | None = None


@admin_router.patch("/mcp/{mcp_id}")
def patch_mcp(mcp_id: str, payload: MCPPatch, principal=Depends(require_admin), db=Depends(get_db)):
    m = db.query(MCPServer).filter(MCPServer.id == mcp_id, MCPServer.org_id == principal.org.id).first()
    if m is None:
        raise HTTPException(status_code=404, detail="not found")
    if payload.name is not None:
        m.name = payload.name
    if payload.transport is not None:
        m.transport = payload.transport
    if payload.config is not None:
        m.config_json = json.dumps(payload.config, ensure_ascii=False)
    if payload.enabled is not None:
        m.enabled = payload.enabled
    write_audit(db, action="mcp.patch", actor_id=principal.user.id, org_id=principal.org.id, target=mcp_id, detail=payload.model_dump(exclude_none=True))
    db.commit(); db.refresh(m)
    return _mcp_to_dict(m)

@admin_router.delete("/mcp/{mcp_id}", status_code=204)
def delete_mcp(mcp_id: str, principal=Depends(require_admin), db=Depends(get_db)):
    m = db.query(MCPServer).filter(MCPServer.id == mcp_id, MCPServer.org_id == principal.org.id).first()
    if m is None:
        raise HTTPException(status_code=404, detail="not found")
    db.delete(m)
    write_audit(db, action="mcp.delete", actor_id=principal.user.id, org_id=principal.org.id, target=mcp_id)
    db.commit()
    return None


# ---------- Plugins ----------
class PluginIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    manifest: Dict[str, Any] = {}
    enabled: bool = True


def _plugin_to_dict(p):
    try:
        manifest = json.loads(p.manifest_json or "{}")
    except Exception:
        manifest = {}
    return {"id": p.id, "name": p.name, "manifest": manifest, "enabled": p.enabled}


@admin_router.get("/plugins")
def list_plugins(principal=Depends(require_admin), db=Depends(get_db)):
    rows = db.query(Plugin).filter(Plugin.org_id == principal.org.id).order_by(Plugin.created_at.asc()).all()
    return [_plugin_to_dict(r) for r in rows]


@admin_router.post("/plugins", status_code=201)
def add_plugin(payload: PluginIn, principal=Depends(require_admin), db=Depends(get_db)):
    p = Plugin(org_id=principal.org.id, name=payload.name, manifest_json=json.dumps(payload.manifest, ensure_ascii=False), enabled=payload.enabled)
    db.add(p)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="plugin name already exists")
    db.refresh(p)
    write_audit(db, action="plugin.create", actor_id=principal.user.id, org_id=principal.org.id, target=p.id)
    db.commit()
    return _plugin_to_dict(p)


class PluginPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    manifest: dict | None = None
    enabled: bool | None = None


@admin_router.patch("/plugins/{plugin_id}")
def patch_plugin(plugin_id: str, payload: PluginPatch, principal=Depends(require_admin), db=Depends(get_db)):
    p = db.query(Plugin).filter(Plugin.id == plugin_id, Plugin.org_id == principal.org.id).first()
    if p is None:
        raise HTTPException(status_code=404, detail="not found")
    if payload.name is not None:
        p.name = payload.name
    if payload.manifest is not None:
        p.manifest_json = json.dumps(payload.manifest, ensure_ascii=False)
    if payload.enabled is not None:
        p.enabled = payload.enabled
    write_audit(db, action="plugin.patch", actor_id=principal.user.id, org_id=principal.org.id, target=plugin_id, detail=payload.model_dump(exclude_none=True))
    db.commit(); db.refresh(p)
    return _plugin_to_dict(p)

@admin_router.delete("/plugins/{plugin_id}", status_code=204)
def delete_plugin(plugin_id: str, principal=Depends(require_admin), db=Depends(get_db)):
    p = db.query(Plugin).filter(Plugin.id == plugin_id, Plugin.org_id == principal.org.id).first()
    if p is None:
        raise HTTPException(status_code=404, detail="not found")
    db.delete(p)
    write_audit(db, action="plugin.delete", actor_id=principal.user.id, org_id=principal.org.id, target=plugin_id)
    db.commit()
    return None


# ---------- Wiki: batch ingest + reset alias ----------
@admin_router.post("/wiki/ingest")
def batch_ingest(principal=Depends(require_admin), db=Depends(get_db)):
    corpus = db.query(WikiCorpus).filter(WikiCorpus.org_id == principal.org.id).first()
    if corpus is None:
        raise HTTPException(status_code=404, detail="wiki corpus not found")
    pending = db.query(WikiSource).filter(WikiSource.corpus_id == corpus.id, WikiSource.status == "pending").all()
    succeeded = 0
    failed = 0
    for src in pending:
        try:
            run_ingest(corpus, src, db)
            src.status = "ingested"
            src.error = None
            db.commit()
            succeeded += 1
        except Exception as e:
            src.status = "failed"
            src.error = str(e)[:500]
            db.commit()
            failed += 1
    write_audit(db, action="wiki.ingest.batch", actor_id=principal.user.id, org_id=principal.org.id, target=corpus.id, detail={"succeeded": succeeded, "failed": failed})
    db.commit()
    return {"ok": True, "succeeded": succeeded, "failed": failed, "total": len(pending)}


@admin_router.post("/wiki/reset")
def wiki_reset_alias(payload: Dict[str, Any] = {}, principal=Depends(require_admin), db=Depends(get_db)):
    return _reset_corpus(principal=principal, db=db)
