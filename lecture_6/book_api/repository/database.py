from typing import Any, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from pathlib import Path

Base = declarative_base()

DB_BOOK = "DB.db"   # in .env ->

BASE_DIR = Path(__file__).parent
DATABASE_URL = f"sqlite+aiosqlite:///{BASE_DIR / DB_BOOK}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    """Asynchronous database session generator for use in FastAPI.

    This generator is used with Depends on make each endpoint
    I got my own asynchronous SQLAlchemy session, which
    closes automatically after exiting the context.

    Yields:
        AsyncSession: Asynchronous SQLAlchemy session for execution
        database queries.
        """
    async with async_session() as session:
        yield session
