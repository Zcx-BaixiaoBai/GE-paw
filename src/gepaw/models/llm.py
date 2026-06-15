"""LLM 终端、技能、MCP、插件、模型网关。"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from ..app.db import Base


def _uuid() -> str:
    return uuid.uuid4().hex


class LLMEndpoint(Base):
    __tablename__ = "llm_endpoint"
    __table_args__ = (
        UniqueConstraint("org_id", "name", name="uq_llm_endpoint_org_name"),
        Index("ix_llm_endpoint_org", "org_id"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(32), ForeignKey("org.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    base_url: Mapped[str] = mapped_column(String(500), nullable=False)
    api_key_enc: Mapped[str] = mapped_column(Text, nullable=False, default="")
    model: Mapped[str] = mapped_column(String(200), nullable=False)
    max_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=4096)
    temperature: Mapped[float] = mapped_column(Float, nullable=False, default=0.2)
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    extra_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class Skill(Base):
    __tablename__ = "skill"
    __table_args__ = (
        UniqueConstraint("org_id", "name", name="uq_skill_org_name"),
        Index("ix_skill_org", "org_id"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(32), ForeignKey("org.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    manifest_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class MCPServer(Base):
    __tablename__ = "mcp_server"
    __table_args__ = (
        UniqueConstraint("org_id", "name", name="uq_mcp_org_name"),
        Index("ix_mcp_org", "org_id"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(32), ForeignKey("org.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    transport: Mapped[str] = mapped_column(String(40), nullable=False, default="stdio")
    config_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class Plugin(Base):
    __tablename__ = "plugin"
    __table_args__ = (
        UniqueConstraint("org_id", "name", name="uq_plugin_org_name"),
        Index("ix_plugin_org", "org_id"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(32), ForeignKey("org.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    manifest_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class GatewayFilter(Base):
    """模型网关屏蔽词规则。

    每条记录代表一个需要过滤的关键词或短语。
    支持精确关键词匹配、语义相似度匹配、正则匹配。
    统计字段记录识别次数、识别率、拦截率。
    """
    __tablename__ = "gateway_filter"
    __table_args__ = (
        Index("ix_gateway_filter_org", "org_id"),
        Index("ix_gateway_filter_enabled", "enabled"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(32), ForeignKey("org.id", ondelete="CASCADE"), nullable=False)
    keyword: Mapped[str] = mapped_column(String(500), nullable=False)
    match_mode: Mapped[str] = mapped_column(String(20), nullable=False, default="exact")
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default="block")
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    detect_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    block_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_checks: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class GatewayLog(Base):
    """模型网关拦截日志。"""
    __tablename__ = "gateway_log"
    __table_args__ = (
        Index("ix_gateway_log_org", "org_id"),
        Index("ix_gateway_log_created", "created_at"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(32), ForeignKey("org.id", ondelete="CASCADE"), nullable=False)
    filter_id: Mapped[str] = mapped_column(String(32), ForeignKey("gateway_filter.id", ondelete="CASCADE"), nullable=False)
    keyword: Mapped[str] = mapped_column(String(500), nullable=False)
    matched_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    match_mode: Mapped[str] = mapped_column(String(20), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    action_taken: Mapped[str] = mapped_column(String(20), nullable=False)
    session_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    model_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
