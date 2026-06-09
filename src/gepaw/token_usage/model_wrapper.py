"""Single entry point for recording LLM token usage.

All LLM call sites (chat, cron, wiki query) call record_usage() exactly once per
LLM call. The wrapper computes cost from the configured cost table and inserts
a TokenUsageLog row.

Usage:
    from gepaw.token_usage import record_usage
    record_usage(
        db, org_id=..., user_id=..., session_id=..., model=...,
        prompt_tokens=..., completion_tokens=...,
    )
"""
from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from ..models import TokenUsageLog
from ..utils.logging import get_logger
from .cost_table import compute_cost_cents

logger = get_logger("token_usage")


def record_usage(
    db: Optional[Session],
    *,
    org_id: str,
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    message_id: Optional[str] = None,
    commit: bool = False,
) -> int:
    """Insert a TokenUsageLog row.

    By default the row is added to the caller's session and flushed but not
    committed; the caller controls the transaction. Set commit=True to commit
    in a fresh short-lived session so the write persists even if the caller's
    transaction is later rolled back (e.g. LLM call raised and converted to 500).
    """
    p = max(0, int(prompt_tokens or 0))
    c = max(0, int(completion_tokens or 0))
    if not org_id:
        logger.warning("record_usage: missing org_id, skipping")
        return 0
    model_name = (model or "unknown").strip() or "unknown"
    cost = compute_cost_cents(model_name, p, c)
    from ..app.db import session_scope
    if commit or db is None:
        try:
            with session_scope() as s:
                entry = TokenUsageLog(
                    org_id=org_id,
                    user_id=user_id,
                    session_id=session_id,
                    message_id=message_id,
                    model=model_name,
                    prompt_tokens=p,
                    completion_tokens=c,
                    total_tokens=p + c,
                    cost_cents=cost,
                )
                s.add(entry)
                s.flush()
                return int(entry.id or 0)
        except Exception as e:
            logger.warning("record_usage failed: %s", e)
            return 0
    try:
        entry = TokenUsageLog(
            org_id=org_id,
            user_id=user_id,
            session_id=session_id,
            message_id=message_id,
            model=model_name,
            prompt_tokens=p,
            completion_tokens=c,
            total_tokens=p + c,
            cost_cents=cost,
        )
        db.add(entry)
        db.flush()
        return int(entry.id or 0)
    except Exception as e:
        logger.warning("record_usage failed: %s", e)
        return 0
