from logging.config import fileConfig
import os 
import sys
from dotenv import load_dotenv # Add this
import asyncio
from sqlalchemy import pool
from sqlalchemy.engine import Connection
# No need for async_engine_from_config if using create_async_engine manually
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from app.infraestructure.database.models import Base

# Ensure the app directory is in the path
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

# --- LOAD ENV DATA ---
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construct the Async URL
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- CONFIG OBJECT ---
config = context.config

# Inject the URL into the alembic config dynamically
config.set_main_option("sqlalchemy.url", ASYNC_DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:

    url = config.get_main_option("sqlalchemy.url")

    context.configure(

        url = url,

        target_metadata = target_metadata,

        literal_binds = True,

        dialect_opts= {"paramstyle": "pyformat"}

    )

    with context.begin_transaction():

        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:

    context.configure(connection=connection, target_metadata=target_metadata)

   

    with context.begin_transaction():

        context.run_migrations()

async def run_async_migrations() -> None:
    # Use the URL we just injected into the config object
    url = config.get_main_option("sqlalchemy.url")
    
    connectable = create_async_engine(
        url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    
    await connectable.dispose()

def run_migrations_online() -> None:
    # Use existing event loop if one is already running, 
    # though asyncio.run is usually fine for the alembic CLI context
    try:
        asyncio.run(run_async_migrations())
    except RuntimeError:
        # Fallback for environments where a loop is already running
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()