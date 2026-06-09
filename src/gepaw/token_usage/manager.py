# -*- coding: utf-8 -*-
"""Token usage manager — thin orchestrator.
"""

import logging
import threading
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from ..constant import WORKING_DIR, TOKEN_USAGE_FILE
from .buffer import TokenUsageBuffer, _UsageEvent

logger = logging.getLogger(__name__)


class TokenUsageStats(BaseModel):
    """Prompt/completion tokens and call count."""

    prompt_tokens: int = Field(0, ge=0)
    completion_tokens: int = Field(0, ge=0)
    call_count: int = Field(0, ge=0)


class TokenUsageRecord(TokenUsageStats):
    """Single row from token usage query (per date + provider + model)."""

    date: str = Field(..., description="Date (YYYY-MM-DD)")
    provider_id: str = Field("", description="Provider ID")
    model: str = Field(..., description="Model name")


class TokenUsageByModel(TokenUsageStats):
    """Per-model aggregate in summary (provider + model + counts)."""

    provider_id: str = Field("", description="Provider ID")
    model: str = Field(..., description="Model name")


class TokenUsageByDateModel(TokenUsageStats):
    """Per-date per-model aggregate in summary."""

    provider_id: str = Field("", description="Provider ID")
    model: str = Field(..., description="Model name")


class TokenUsageSummary(BaseModel):
    """Aggregated token usage summary returned by get_summary()."""

    total_prompt_tokens: int = Field(0, ge=0)
    total_completion_tokens: int = Field(0, ge=0)
    total_calls: int = Field(0, ge=0)
    by_model: dict[str, TokenUsageByModel] = Field(
        default_factory=dict,
        description="Per model (provider:model key) aggregation",
    )
    by_date: dict[str, TokenUsageStats] = Field(
        default_factory=dict,
        description="Per date (YYYY-MM-DD) - all models combined",
    )


class TokenUsageManager:
    """Orchestrator for token usage recording and querying."""

    _instance: "TokenUsageManager | None" = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        path: Path = (WORKING_DIR / TOKEN_USAGE_FILE).expanduser()
        self._buffer = TokenUsageBuffer(path)
        self._flush_interval = 10  # default

    def start(self, flush_interval: int = 10) -> None:
        """Start background flush task.

        Must be called from an async context (e.g. app lifespan startup).
        ``flush_interval`` is the number of seconds between flushes.
        """
        self._flush_interval = flush_interval
        # Recreate buffer with desired flush_interval if different from default
        if flush_interval != 10:
            path: Path = (WORKING_DIR / TOKEN_USAGE_FILE).expanduser()
            self._buffer = TokenUsageBuffer(
                path,
                flush_interval=flush_interval,
            )
        self._buffer.start()

    async def stop(self) -> None:
        """Stop the flush task and perform a final flush before exit."""
        await self._buffer.stop()

    def enqueue(self, event: _UsageEvent) -> None:
        """Synchronous fire-and-forget — enqueue a pre-built usage event.

        Called directly from ``TokenRecordingModelWrapper._record_usage()``
        on the hot path. No ``await`` required.
        """
        self._buffer.enqueue(event)

    async def record(
        self,
        provider_id: str,
        model_name: str,
        prompt_tokens: int,
        completion_tokens: int,
        at_date: Optional[date] = None,
    ) -> None:
        """Record token usage for a given provider, model and date.

        Convenience async wrapper around ``enqueue()`` for callers that
        prefer the original async interface (e.g. tests, skill tools).

        Args:
            provider_id: ID of the provider (e.g. "dashscope", "openai").
            model_name: Name of the model (e.g. "qwen3-max", "gpt-4").
            prompt_tokens: Number of input/prompt tokens.
            completion_tokens: Number of output/completion tokens.
            at_date: Date to record under. Defaults to today (local).
        """
        from datetime import datetime, timezone

        if at_date is None:
            at_date = date.today()
        self._buffer.enqueue(
            _UsageEvent(
                provider_id=provider_id,
                model_name=model_name,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                date_str=at_date.isoformat(),
                now_iso=datetime.now(tz=timezone.utc).isoformat(
                    timespec="seconds",
                ),
            ),
        )

    async def _query(
        self,
        merged: dict,
        start_date: date,
        end_date: date,
        model_name: Optional[str],
        provider_id: Optional[str],
    ) -> list[TokenUsageRecord]:
        """Return per-day records from the merged data dict."""
        results: list[TokenUsageRecord] = []

        current = start_date
        while current <= end_date:
            date_str = current.isoformat()
            by_key = merged.get(date_str, {})
            for _key, entry in by_key.items():
                rec_provider = entry.get("provider_id", "")
                rec_model = entry.get("model_name") or _key
                if model_name is not None and rec_model != model_name:
                    continue
                if provider_id is not None and rec_provider != provider_id:
                    continue
                results.append(
                    TokenUsageRecord(
                        date=date_str,
                        provider_id=rec_provider,
                        model=rec_model,
                        prompt_tokens=entry.get("prompt_tokens", 0),
                        completion_tokens=entry.get("completion_tokens", 0),
                        call_count=entry.get("call_count", 0),
                    ),
                )
            current += timedelta(days=1)

        return results

    async def get_summary(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        model_name: Optional[str] = None,
        provider_id: Optional[str] = None,
    ) -> TokenUsageSummary:
        """Get aggregated token usage summary.

        Args:
            start_date: Start of date range (inclusive). Default: 30 days ago.
            end_date: End of date range (inclusive). Default: today.
            model_name: Optional model name filter.
            provider_id: Optional provider ID filter.

        Returns:
            TokenUsageSummary with totals, by_model, by_provider, by_date.
        """
        if end_date is None:
            end_date = date.today()
        if start_date is None:
            start_date = end_date - timedelta(days=30)

        merged = await self._buffer.get_merged_data()

        records = await self._query(
            merged,
            start_date,
            end_date,
            model_name,
            provider_id,
        )

        total_prompt = 0
        total_completion = 0
        total_calls = 0
        by_model_raw: dict[str, dict] = {}
        by_date_raw: dict[str, dict] = {}

        for r in records:
            pt = r.prompt_tokens
            ct = r.completion_tokens
            calls = r.call_count
            total_prompt += pt
            total_completion += ct
            total_calls += calls

            # Aggregate by model
            model_key = (
                f"{r.provider_id}:{r.model}" if r.provider_id else r.model
            )
            bm = by_model_raw.setdefault(
                model_key,
                {
                    "provider_id": r.provider_id,
                    "model": r.model,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "call_count": 0,
                },
            )
            bm["prompt_tokens"] += pt
            bm["completion_tokens"] += ct
            bm["call_count"] += calls

            # Aggregate by date
            bd = by_date_raw.setdefault(
                r.date,
                {"prompt_tokens": 0, "completion_tokens": 0, "call_count": 0},
            )
            bd["prompt_tokens"] += pt
            bd["completion_tokens"] += ct
            bd["call_count"] += calls

        return TokenUsageSummary(
            total_prompt_tokens=total_prompt,
            total_completion_tokens=total_completion,
            total_calls=total_calls,
            by_model={
                k: TokenUsageByModel.model_validate(v)
                for k, v in sorted(by_model_raw.items())
            },
            by_date={
                k: TokenUsageStats.model_validate(v)
                for k, v in sorted(by_date_raw.items())
            },
        )

    async def get_details(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        model_name: Optional[str] = None,
        provider_id: Optional[str] = None,
    ) -> list[TokenUsageRecord]:
        """Get raw token usage records for frontend aggregation.

        Args:
            start_date: Start of date range (inclusive). Default: 30 days ago.
            end_date: End of date range (inclusive). Default: today.
            model_name: Optional model name filter.
            provider_id: Optional provider ID filter.

        Returns:
            List of TokenUsageRecord with per-date per-model data.
        """
        if end_date is None:
            end_date = date.today()
        if start_date is None:
            start_date = end_date - timedelta(days=30)

        merged = await self._buffer.get_merged_data()

        records = await self._query(
            merged,
            start_date,
            end_date,
            model_name,
            provider_id,
        )

        return records

    @classmethod
    def get_instance(cls) -> "TokenUsageManager":
        """Return the process-wide singleton ``TokenUsageManager``."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance


def get_token_usage_manager() -> TokenUsageManager:
    """Return the process-wide singleton ``TokenUsageManager``."""
    return TokenUsageManager.get_instance()


# --- DB-backed query helpers (sync) -----------------------------------------


def _db_rows(db, org_id):
    """Iterate TokenUsageLog rows scoped to ``org_id``."""
    try:
        from ..models.assistant import TokenUsageLog
    except Exception:
        return []
    q = db.query(TokenUsageLog).filter(TokenUsageLog.org_id == org_id)
    return q.all()


def summarize(db, org_id):
    """Totals for an org. Sync, DB-backed."""
    rows = _db_rows(db, org_id)
    pt = sum(int(getattr(r, "prompt_tokens", 0) or 0) for r in rows)
    ct = sum(int(getattr(r, "completion_tokens", 0) or 0) for r in rows)
    cost = sum(int(getattr(r, "cost_cents", 0) or 0) for r in rows)
    return {
        "prompt_tokens": pt,
        "completion_tokens": ct,
        "cost_cents": cost,
        "calls": len(rows),
    }


def by_model(db, org_id):
    """Per-model totals."""
    rows = _db_rows(db, org_id)
    out = {}
    for r in rows:
        m = getattr(r, "model", "") or ""
        agg = out.setdefault(m, {"model": m, "prompt_tokens": 0, "completion_tokens": 0, "cost_cents": 0, "calls": 0})
        agg["prompt_tokens"] += int(getattr(r, "prompt_tokens", 0) or 0)
        agg["completion_tokens"] += int(getattr(r, "completion_tokens", 0) or 0)
        agg["cost_cents"] += int(getattr(r, "cost_cents", 0) or 0)
        agg["calls"] += 1
    return list(out.values())


def by_user(db, org_id):
    """Per-user totals."""
    rows = _db_rows(db, org_id)
    out = {}
    for r in rows:
        u = getattr(r, "user_id", None)
        u = str(u) if u is not None else ""
        agg = out.setdefault(u, {"user_id": u, "prompt_tokens": 0, "completion_tokens": 0, "cost_cents": 0, "calls": 0})
        agg["prompt_tokens"] += int(getattr(r, "prompt_tokens", 0) or 0)
        agg["completion_tokens"] += int(getattr(r, "completion_tokens", 0) or 0)
        agg["cost_cents"] += int(getattr(r, "cost_cents", 0) or 0)
        agg["calls"] += 1
    return list(out.values())


def by_day(db, org_id):
    """Per-day totals. Returns list of objects with .total_tokens/.call_count."""
    rows = _db_rows(db, org_id)
    out = {}
    for r in rows:
        ts = getattr(r, "occurred_at", None)
        if ts is None:
            day = ""
        else:
            day = ts.strftime("%Y-%m-%d") if hasattr(ts, "strftime") else str(ts)[:10]
        agg = out.setdefault(day, {"date": day, "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "call_count": 0})
        agg["prompt_tokens"] += int(getattr(r, "prompt_tokens", 0) or 0)
        agg["completion_tokens"] += int(getattr(r, "completion_tokens", 0) or 0)
        agg["total_tokens"] = agg["prompt_tokens"] + agg["completion_tokens"]
        agg["call_count"] += 1
    out_list = list(out.values())
    out_list.sort(key=lambda x: x.get("date") or "")

    class _Bucket:
        def __init__(self, d):
            for k, v in d.items():
                setattr(self, k, v)
    return [_Bucket(d) for d in out_list]


def get_summary(db, org_id):
    """Backwards-compatible alias used by some call sites."""
    return summarize(db, org_id)


def get_details(db, org_id):
    """Return raw rows as dicts."""
    rows = _db_rows(db, org_id)
    out = []
    for r in rows:
        out.append({
            "id": getattr(r, "id", None),
            "org_id": getattr(r, "org_id", None),
            "user_id": getattr(r, "user_id", None),
            "session_id": getattr(r, "session_id", None),
            "model": getattr(r, "model", None),
            "prompt_tokens": getattr(r, "prompt_tokens", 0),
            "completion_tokens": getattr(r, "completion_tokens", 0),
            "total_tokens": (int(getattr(r, "prompt_tokens", 0) or 0) + int(getattr(r, "completion_tokens", 0) or 0)),
            "cost_cents": getattr(r, "cost_cents", 0),
        })
    return out
