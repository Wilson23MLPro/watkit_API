import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.infraestructure.database.models import Base
from pathlib import Path

#this finds the .evn file in the project root regardless of where you run the script from
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


#Build the PostgreSQL Async URL
# Format: postgresql+asyncpg://user:password@host:port/dbname
DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
print("DATABASE_URL:", DATABASE_URL)
# engine setup

# Create the async engine for database connections
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session factory bound to the engine
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# Initialize the database (create tables if they don't exist)
async def init_db():
    # Open an async transaction with the engine
    async with engine.begin() as conn:
        # Note: With Postgres, ensure the database  already exists
        # Create all tables defined in the SQLAlchemy models
        await conn.run_sync(Base.metadata.create_all)

# Dependency to get a database session (for use in routes/services)
async def get_db():
    # Open an async session
    async with SessionLocal() as session:
        try:
            # Yield the session to the caller
            yield session
        finally:
            # Ensure the session is closed after use
            await session.close()