"""add chat_session.permission

Stores the per-session Codex-style permission mode picked by the user in
the chat composer. Values: full | smart | strict | readonly | null.
null means "follow the global ToolExecutionLevel default".
"""
from __future__ import annotations

revision = "0002_add_chat_session_permission"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None

from alembic import op  # noqa: E402
import sqlalchemy as sa  # noqa: E402


def upgrade() -> None:
    bind = op.get_bind()
    cols = {row[1] for row in bind.execute(sa.text("PRAGMA table_info(chat_session)")).fetchall()} \
        if bind.dialect.name == "sqlite" else {c["name"] for c in sa.inspect(bind).get_columns("chat_session")}
    if "permission" not in cols:
        with op.batch_alter_table("chat_session") as batch_op:
            batch_op.add_column(sa.Column("permission", sa.String(length=20), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("chat_session") as batch_op:
        batch_op.drop_column("permission")
