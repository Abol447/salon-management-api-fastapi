from logging.config import fileConfig

import os
from pathlib import Path

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from app.models import *
from app.db.base import Base

# ============================================================
# Load .env
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE, override=True)


# ============================================================
# Alembic Config
# ============================================================

config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# ============================================================
# SQLAlchemy Metadata
# ============================================================

target_metadata = Base.metadata


# ============================================================
# Database URL
# ============================================================


def get_database_url() -> str:
    host = os.getenv("DATABASE_HOST")
    port = os.getenv("DATABASE_PORT")
    user = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD", "")
    database = os.getenv("DATABASE_NAME")

    # Password can be empty for local MySQL
    if not all([host, port, user, database]):
        raise RuntimeError(
            "Database configuration is incomplete. "
            f"HOST={host}, "
            f"PORT={port}, "
            f"USER={user}, "
            f"DATABASE={database}"
        )

    return f"mysql+pymysql://" f"{user}:{password}@{host}:{port}/{database}"


# ============================================================
# Offline Migration
# ============================================================


def run_migrations_offline() -> None:
    url = get_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ============================================================
# Online Migration
# ============================================================


def run_migrations_online() -> None:
    database_url = get_database_url()

    configuration = config.get_section(
        config.config_ini_section,
        {},
    )

    configuration["sqlalchemy.url"] = database_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ============================================================
# Run
# ============================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
