from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

DATABASE_URL = "sqlite+aiosqlite:///./ecomute.db"

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to True for SQL query logging, can be set to False in production
)


# SQLite needs this to enforce foreign keys (ON DELETE, etc.)
@event.listens_for(engine.sync_engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]: # This function is a FastAPI dependency that provides a database session to route handlers. It creates a new session for each request and ensures that it is properly closed after the request is processed.
    async with AsyncSessionLocal() as session:
        yield session
