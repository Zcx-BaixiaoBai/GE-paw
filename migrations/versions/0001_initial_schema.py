"""initial schema

GE-paw v1 schema. Hand-written because autogenerate produced an empty file in
this environment; we use Base.metadata.create_all on an empty database to make
the initial revision the single source of truth for the schema, then any
later schema change goes through a normal alembic revision.
"""
from __future__ import annotations

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None

from alembic import op  # noqa: E402

# Mirror the SQLAlchemy declarative models so the initial revision is the
# authoritative source of truth for the v1 schema.
import sys, pathlib  # noqa: E402
_REPO = pathlib.Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from src.gepaw.app.db import Base, get_engine  # noqa: E402
import src.gepaw.models  # noqa: E402,F401  -- register all tables


def upgrade() -> None:
    bind = op.get_bind()
    # SQLite needs batch mode for ALTER operations; create_all is fine for an
    # initial empty database and keeps the schema identical to Base.metadata.
    Base.metadata.create_all(bind)


def downgrade() -> None:
    bind = op.get_bind()
    # Drop every table GE-paw owns. Order is irrelevant with cascade on the FKs.
    Base.metadata.drop_all(bind)
