from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
import os
import sys

# Add app path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
from app.config import get_settings
from app.database import Base
from app import models  # ensure models are imported

# Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# Set metadata and load .env config
target_metadata = Base.metadata
settings = get_settings()

# Use psycopg2 (sync) for Alembic migrations
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("asyncpg", "psycopg2"))


def run_migrations_offline():
    """Run migrations without a live DB connection (generates SQL)."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations with DB connection."""
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()