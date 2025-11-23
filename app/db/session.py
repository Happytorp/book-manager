from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import SessionLocal


async def get_db() -> AsyncSession:
    """Dependency for getting async database sessions."""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
