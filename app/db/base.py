from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from app.config import settings

DATABASE_URL = settings.get_database_url()

engine = create_async_engine(
    DATABASE_URL, 
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=True,
    autocommit=False
)

Base = declarative_base()
