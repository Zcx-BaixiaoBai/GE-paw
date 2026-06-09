"""Read-side helpers for token usage: aggregation queries and monthly quotas."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import TokenUsageLog


@dataclass
class UsageBucket:
    bucket: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_cents: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bucket": self.bucket,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "cost_cents": self.cost_cents,
        }


def _date_trunc_sql(db: Session) -> Any:
    bind = db.get_bind()
    dialect = bind.dialect.name if bind is not None else ""
    if dialect.startswith("postgres"):
        return func.date_trunc("day", TokenUsageLog.occurred_at)
    return func.strftime("%Y-%m-%d", TokenUsageLog.occurred_at)


def summarize(db: Session, org_id: str, since: Optional[datetime] = None) -> Dict[str, Any]:
    q = db.query(TokenUsageLog).filter(TokenUsageLog.org_id == org_id)
    if since is not None:
        q = q.filter(TokenUsageLog.occurred_at >= since)
    rows = q.all()
    pt = sum(r.prompt_tokens for r in rows)
    ct = sum(r.completion_tokens for r in rows)
    cost = sum(r.cost_cents for r in rows)
    return {
        "prompt_tokens": pt,
        "completion_tokens": ct,
        "total_tokens": pt + ct,
        "cost_cents": cost,
        "calls": len(rows),
    }


def by_day(db: Session, org_id: str, since: Optional[datetime] = None) -> List[UsageBucket]:
    trunc = _date_trunc_sql(db)
    q = (
        db.query(
            trunc.label("bucket"),
            func.coalesce(func.sum(TokenUsageLog.prompt_tokens), 0).label("pt"),
            func.coalesce(func.sum(TokenUsageLog.completion_tokens), 0).label("ct"),
            func.coalesce(func.sum(TokenUsageLog.total_tokens), 0).label("tt"),
            func.coalesce(func.sum(TokenUsageLog.cost_cents), 0).label("cc"),
        )
        .filter(TokenUsageLog.org_id == org_id)
        .group_by("bucket")
        .order_by("bucket")
    )
    if since is not None:
        q = q.filter(TokenUsageLog.occurred_at >= since)
    out: List[UsageBucket] = []
    for bucket, pt, ct, tt, cc in q.all():
        out.append(UsageBucket(str(bucket), int(pt or 0), int(ct or 0), int(tt or 0), int(cc or 0)))
    return out


def by_user(db: Session, org_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    rows = (
        db.query(
            TokenUsageLog.user_id,
            func.coalesce(func.sum(TokenUsageLog.prompt_tokens), 0).label("pt"),
            func.coalesce(func.sum(TokenUsageLog.completion_tokens), 0).label("ct"),
            func.coalesce(func.sum(TokenUsageLog.cost_cents), 0).label("cc"),
            func.count(TokenUsageLog.id).label("calls"),
        )
        .filter(TokenUsageLog.org_id == org_id)
        .group_by(TokenUsageLog.user_id)
        .order_by(func.count(TokenUsageLog.id).desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "user_id": r.user_id,
            "prompt_tokens": int(r.pt or 0),
            "completion_tokens": int(r.ct or 0),
            "cost_cents": int(r.cc or 0),
            "calls": int(r.calls or 0),
        }
        for r in rows
    ]


def by_model(db: Session, org_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    rows = (
        db.query(
            TokenUsageLog.model,
            func.coalesce(func.sum(TokenUsageLog.prompt_tokens), 0).label("pt"),
            func.coalesce(func.sum(TokenUsageLog.completion_tokens), 0).label("ct"),
            func.coalesce(func.sum(TokenUsageLog.cost_cents), 0).label("cc"),
            func.count(TokenUsageLog.id).label("calls"),
        )
        .filter(TokenUsageLog.org_id == org_id)
        .group_by(TokenUsageLog.model)
        .order_by(func.count(TokenUsageLog.id).desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "model": r.model,
            "prompt_tokens": int(r.pt or 0),
            "completion_tokens": int(r.ct or 0),
            "cost_cents": int(r.cc or 0),
            "calls": int(r.calls or 0),
        }
        for r in rows
    ]


def month_to_date(db: Session, org_id: str, now: Optional[datetime] = None) -> Dict[str, Any]:
    now = now or datetime.now(timezone.utc).replace(tzinfo=None)
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return summarize(db, org_id, since=start)


def last_days(db: Session, org_id: str, days: int = 30) -> Dict[str, Any]:
    since = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=max(1, days))
    return summarize(db, org_id, since=since)
