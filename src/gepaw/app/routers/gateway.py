# -*- coding: utf-8 -*-
"""模型网关管理 API 路由。

提供屏蔽词规则的 CRUD、统计查询、拦截日志查询。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import desc
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import Principal, require_admin
from ...models.llm import GatewayFilter, GatewayLog

router = APIRouter(prefix="/gateway", tags=["gateway"])


# ---------- Request/Response 模型 ----------

class FilterCreate(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=500)
    match_mode: str = Field(default="exact", pattern="^(exact|regex|semantic)$")
    severity: str = Field(default="block", pattern="^(block|warn|log)$")
    category: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None)
    enabled: bool = Field(default=True)


class FilterUpdate(BaseModel):
    keyword: Optional[str] = Field(default=None, min_length=1, max_length=500)
    match_mode: Optional[str] = Field(default=None, pattern="^(exact|regex|semantic)$")
    severity: Optional[str] = Field(default=None, pattern="^(block|warn|log)$")
    category: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None)
    enabled: Optional[bool] = Field(default=None)


class FilterResponse(BaseModel):
    id: str
    keyword: str
    match_mode: str
    severity: str
    category: Optional[str]
    description: Optional[str]
    enabled: bool
    detect_count: int
    block_count: int
    total_checks: int
    detect_rate: float
    block_rate: float
    created_at: str
    updated_at: str


class GatewayStats(BaseModel):
    total_filters: int
    enabled_filters: int
    total_detections: int
    total_blocks: int
    total_checks: int
    overall_detect_rate: float
    overall_block_rate: float


class LogResponse(BaseModel):
    id: str
    filter_id: str
    keyword: str
    matched_text: str
    match_mode: str
    severity: str
    action_taken: str
    session_id: Optional[str]
    user_id: Optional[str]
    model_name: Optional[str]
    created_at: str


def _to_filter_response(f: GatewayFilter) -> dict:
    total = f.total_checks or 0
    detect_rate = round(f.detect_count / total, 4) if total > 0 else 0.0
    block_rate = round(f.block_count / total, 4) if total > 0 else 0.0
    return {
        "id": f.id,
        "keyword": f.keyword,
        "match_mode": f.match_mode,
        "severity": f.severity,
        "category": f.category,
        "description": f.description,
        "enabled": f.enabled,
        "detect_count": f.detect_count,
        "block_count": f.block_count,
        "total_checks": f.total_checks,
        "detect_rate": detect_rate,
        "block_rate": block_rate,
        "created_at": f.created_at.isoformat() if f.created_at else "",
        "updated_at": f.updated_at.isoformat() if f.updated_at else "",
    }


# ---------- CRUD ----------

@router.get("/filters", response_model=List[FilterResponse])
def list_filters(
    principal: Principal = Depends(require_admin),
    db: Session = Depends(get_db),
    enabled_only: bool = False,
    category: Optional[str] = None,
):
    """列出所有屏蔽词规则。"""
    q = db.query(GatewayFilter).filter(GatewayFilter.org_id == principal.user.org_id)
    if enabled_only:
        q = q.filter(GatewayFilter.enabled == True)
    if category:
        q = q.filter(GatewayFilter.category == category)
    rows = q.order_by(GatewayFilter.created_at.desc()).all()
    return [_to_filter_response(f) for f in rows]


@router.post("/filters", response_model=FilterResponse, status_code=201)
def create_filter(
    payload: FilterCreate,
    principal: Principal = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """创建新的屏蔽词规则。"""
    f = GatewayFilter(
        org_id=principal.user.org_id,
        keyword=payload.keyword,
        match_mode=payload.match_mode,
        severity=payload.severity,
        category=payload.category,
        description=payload.description,
        enabled=payload.enabled,
    )
    db.add(f)
    db.commit()
    db.refresh(f)
    return _to_filter_response(f)


@router.put("/filters/{filter_id}", response_model=FilterResponse)
def update_filter(
    filter_id: str,
    payload: FilterUpdate,
    principal: Principal = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """更新屏蔽词规则。"""
    f = db.get(GatewayFilter, filter_id)
    if f is None or f.org_id != principal.user.org_id:
        raise HTTPException(status_code=404, detail="规则不存在")
    for field in ["keyword", "match_mode", "severity", "category", "description", "enabled"]:
        val = getattr(payload, field, None)
        if val is not None:
            setattr(f, field, val)
    db.commit()
    db.refresh(f)
    return _to_filter_response(f)


@router.delete("/filters/{filter_id}", status_code=204)
def delete_filter(
    filter_id: str,
    principal: Principal = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """删除屏蔽词规则。"""
    f = db.get(GatewayFilter, filter_id)
    if f is None or f.org_id != principal.user.org_id:
        raise HTTPException(status_code=404, detail="规则不存在")
    db.delete(f)
    db.commit()


@router.post("/filters/{filter_id}/reset-stats", response_model=FilterResponse)
def reset_filter_stats(
    filter_id: str,
    principal: Principal = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """重置单条规则的统计数据。"""
    f = db.get(GatewayFilter, filter_id)
    if f is None or f.org_id != principal.user.org_id:
        raise HTTPException(status_code=404, detail="规则不存在")
    f.detect_count = 0
    f.block_count = 0
    f.total_checks = 0
    db.commit()
    db.refresh(f)
    return _to_filter_response(f)


# ---------- 统计 ----------

@router.get("/stats", response_model=GatewayStats)
def get_stats(
    principal: Principal = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """获取网关全局统计。"""
    org_id = principal.user.org_id
    filters = db.query(GatewayFilter).filter(GatewayFilter.org_id == org_id).all()
    total = len(filters)
    enabled = sum(1 for f in filters if f.enabled)
    total_detect = sum(f.detect_count for f in filters)
    total_block = sum(f.block_count for f in filters)
    total_checks = sum(f.total_checks for f in filters)
    detect_rate = round(total_detect / total_checks, 4) if total_checks > 0 else 0.0
    block_rate = round(total_block / total_checks, 4) if total_checks > 0 else 0.0
    return GatewayStats(
        total_filters=total,
        enabled_filters=enabled,
        total_detections=total_detect,
        total_blocks=total_block,
        total_checks=total_checks,
        overall_detect_rate=detect_rate,
        overall_block_rate=block_rate,
    )


# ---------- 日志 ----------

@router.get("/logs", response_model=List[LogResponse])
def list_logs(
    principal: Principal = Depends(require_admin),
    db: Session = Depends(get_db),
    limit: int = 100,
    offset: int = 0,
    severity: Optional[str] = None,
    filter_id: Optional[str] = None,
):
    """查询拦截日志。"""
    q = db.query(GatewayLog).filter(GatewayLog.org_id == principal.user.org_id)
    if severity:
        q = q.filter(GatewayLog.severity == severity)
    if filter_id:
        q = q.filter(GatewayLog.filter_id == filter_id)
    rows = q.order_by(desc(GatewayLog.created_at)).offset(offset).limit(limit).all()
    return [
        {
            "id": r.id,
            "filter_id": r.filter_id,
            "keyword": r.keyword,
            "matched_text": r.matched_text[:200],
            "match_mode": r.match_mode,
            "severity": r.severity,
            "action_taken": r.action_taken,
            "session_id": r.session_id,
            "user_id": r.user_id,
            "model_name": r.model_name,
            "created_at": r.created_at.isoformat() if r.created_at else "",
        }
        for r in rows
    ]


@router.delete("/logs", status_code=204)
def clear_logs(
    principal: Principal = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """清空拦截日志。"""
    db.query(GatewayLog).filter(GatewayLog.org_id == principal.user.org_id).delete()
    db.commit()
