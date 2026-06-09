"""助手模式：会话、消息、频道、cron、token 计量。"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from ..app.db import Base


def _uuid() -> str:
    return uuid.uuid4().hex


class ChatSession(Base):
    __tablename__ = "chat_session"
    __table_args__ = (
        Index("ix_chatsession_org", "org_id"),
        Index("ix_chatsession_user", "user_id"),
        Index("ix_chatsession_lastmsg", "last_message_at"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(32), ForeignKey("org.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False, default="新会话")
    channel_kind: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    channel_account_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    pinned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    last_message_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class Message(Base):
    __tablename__ = "message"
    __table_args__ = (
        Index("ix_message_session", "session_id"),
        Index("ix_message_created", "created_at"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    session_id: Mapped[str] = mapped_column(String(32), ForeignKey("chat_session.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False, default="")
    tool_calls_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tokens_in: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tokens_out: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class ChannelAccount(Base):
    __tablename__ = "channel_account"
    __table_args__ = (
        UniqueConstraint("org_id", "kind", "name", name="uq_channel_org_kind_name"),
        Index("ix_channel_org", "org_id"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(32), ForeignKey("org.id", ondelete="CASCADE"), nullable=False)
    kind: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    credentials_enc: Mapped[str] = mapped_column(Text, nullable=False, default="")
    config_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class CronJob(Base):
    __tablename__ = "cron_job"
    __table_args__ = (
        Index("ix_cron_org", "org_id"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(32), ForeignKey("org.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    schedule_cron: Mapped[str] = mapped_column(String(80), nullable=False)
    prompt_template: Mapped[str] = mapped_column(Text, nullable=False)
    target_session_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    target_channel_account_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    failure_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    last_run_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    next_run_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class CronRun(Base):
    __tablename__ = "cron_run"
    __table_args__ = (
        Index("ix_cronrun_job", "cron_id"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    cron_id: Mapped[str] = mapped_column(String(32), ForeignKey("cron_job.id", ondelete="CASCADE"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="running")
    output_excerpt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tokens_in: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tokens_out: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class TokenUsageLog(Base):
    __tablename__ = "token_usage_log"
    __table_args__ = (
        Index("ix_usage_org_time", "org_id", "occurred_at"),
        Index("ix_usage_user_time", "user_id", "occurred_at"),
        Index("ix_usage_model_time", "model", "occurred_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    org_id: Mapped[str] = mapped_column(String(32), ForeignKey("org.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    session_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    message_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    model: Mapped[str] = mapped_column(String(120), nullable=False)
    prompt_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cost_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
