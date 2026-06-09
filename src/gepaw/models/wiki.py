"""问答模式：语料、源、查询日志。"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ..app.db import Base


def _uuid() -> str:
    return uuid.uuid4().hex


class WikiCorpus(Base):
    __tablename__ = "wiki_corpus"
    __table_args__ = (
        Index("ix_wiki_corpus_org", "org_id"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(32), ForeignKey("org.id", ondelete="CASCADE"), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, default="default")
    root_path: Mapped[str] = mapped_column(String(500), nullable=False)
    storage_kind: Mapped[str] = mapped_column(String(20), nullable=False, default="fs")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class WikiSource(Base):
    __tablename__ = "wiki_source"
    __table_args__ = (
        Index("ix_wiki_src_corpus", "corpus_id"),
        Index("ix_wiki_src_status", "status"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    corpus_id: Mapped[str] = mapped_column(String(32), ForeignKey("wiki_corpus.id", ondelete="CASCADE"), nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    path: Mapped[str] = mapped_column(String(500), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mime: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    last_ingested_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class WikiQueryLog(Base):
    __tablename__ = "wiki_query_log"
    __table_args__ = (
        Index("ix_wiki_query_corpus", "corpus_id", "created_at"),
        Index("ix_wiki_query_user", "user_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    corpus_id: Mapped[str] = mapped_column(String(32), ForeignKey("wiki_corpus.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    query: Mapped[str] = mapped_column(Text, nullable=False)
    answer_excerpt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    citations_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tokens_in: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tokens_out: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
