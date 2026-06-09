from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# gepaw integration: use our existing Base + get_settings().database_url
import sys, pathlib
_repo = pathlib.Path(__file__).resolve().parent.parent
if str(_repo) not in sys.path:
    sys.path.insert(0, str(_repo))

from src.gepaw.app.db import Base  # noqa: E402
from src.gepaw.app.settings import get_settings  # noqa: E402
import src.gepaw.models  # noqa: E402,F401  -- ensure all models are registered on Base.metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Inject runtime database url from gepaw settings (overrides alembic.ini value).
# Re-read on every call so test fixtures that swap env vars mid-process pick up
# the new database without reloading this module.
config.set_main_option("sqlalchemy.url", get_settings().database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# gepaw Base.metadata for autogenerate support.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Always re-read settings so env changes are reflected in offline mode too.
    url = get_settings().database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Re-read settings on every online run; the URL from .ini / set_main_option
    # may be stale after the test process monkeypatches env vars.
    config.set_main_option("sqlalchemy.url", get_settings().database_url)
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    # Drop the connection so the next run (which may target a different file)
    # does not inherit stale handles, especially on Windows where SQLite fd
    # release is delayed.
    try:
        connectable.dispose()
    except Exception:
        pass


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
