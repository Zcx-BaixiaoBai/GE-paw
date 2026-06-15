"""add gateway_filter and gateway_log tables

Revision ID: 0003
Revises: 0002
Create Date: 2026-06-15
"""
from __future__ import annotations

revision = "0003_add_gateway_tables"
down_revision = "0002_add_chat_session_permission"
branch_labels = None
depends_on = None

from alembic import op  # noqa: E402
import sqlalchemy as sa  # noqa: E402


def upgrade() -> None:
    bind = op.get_bind()
    from sqlalchemy import inspect as sa_inspect
    existing = set(sa_inspect(bind).get_table_names())

    if "gateway_filter" not in existing:
        op.create_table(
            "gateway_filter",
            sa.Column("id", sa.String(32), primary_key=True),
            sa.Column("org_id", sa.String(32), sa.ForeignKey("org.id", ondelete="CASCADE"), nullable=False),
            sa.Column("keyword", sa.String(500), nullable=False),
            sa.Column("match_mode", sa.String(20), nullable=False, server_default="exact"),
            sa.Column("severity", sa.String(20), nullable=False, server_default="block"),
            sa.Column("category", sa.String(100), nullable=True),
            sa.Column("description", sa.Text, nullable=True),
            sa.Column("enabled", sa.Boolean, nullable=False, server_default=sa.text("1")),
            sa.Column("detect_count", sa.Integer, nullable=False, server_default=sa.text("0")),
            sa.Column("block_count", sa.Integer, nullable=False, server_default=sa.text("0")),
            sa.Column("total_checks", sa.Integer, nullable=False, server_default=sa.text("0")),
            sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        )
        op.create_index("ix_gateway_filter_org", "gateway_filter", ["org_id"])
        op.create_index("ix_gateway_filter_enabled", "gateway_filter", ["enabled"])

    if "gateway_log" not in existing:
        op.create_table(
            "gateway_log",
            sa.Column("id", sa.String(32), primary_key=True),
            sa.Column("org_id", sa.String(32), sa.ForeignKey("org.id", ondelete="CASCADE"), nullable=False),
            sa.Column("filter_id", sa.String(32), sa.ForeignKey("gateway_filter.id", ondelete="CASCADE"), nullable=False),
            sa.Column("keyword", sa.String(500), nullable=False),
            sa.Column("matched_text", sa.Text, nullable=False, server_default=""),
            sa.Column("match_mode", sa.String(20), nullable=False),
            sa.Column("severity", sa.String(20), nullable=False),
            sa.Column("action_taken", sa.String(20), nullable=False),
            sa.Column("session_id", sa.String(32), nullable=True),
            sa.Column("user_id", sa.String(32), nullable=True),
            sa.Column("model_name", sa.String(200), nullable=True),
            sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        )
        op.create_index("ix_gateway_log_org", "gateway_log", ["org_id"])
        op.create_index("ix_gateway_log_created", "gateway_log", ["created_at"])


def downgrade() -> None:
    op.drop_table("gateway_log")
    op.drop_table("gateway_filter")
