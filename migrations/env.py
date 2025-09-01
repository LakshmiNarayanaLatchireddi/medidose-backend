# migrations/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os, sys

# Load .env so DATABASE_URL is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Put project root on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ⬇️ Import the shared Base and ALL models so metadata is populated
from app.utils.db import Base
from app.models import user, patient, medication, prescription

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Alembic will autogenerate from this:
target_metadata = Base.metadata

def run_migrations_offline():
    url = os.getenv("DATABASE_URL")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        {"sqlalchemy.url": os.getenv("DATABASE_URL")},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
