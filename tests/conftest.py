import sys
from pathlib import Path
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models.models import User, Book
from app.api.routers.auth import get_password_hash

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://akshay:123456789@localhost:5432/postgres"

# Create test engine with NullPool to avoid connection issues
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Create a fresh database session for each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session
        await session.rollback()
        await session.close()


async def override_get_db():
    """Override the get_db dependency."""
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session):
    """Create test client with dependency override."""
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session):
    """Create a test user."""
    user = User(
        username="admin",
        email="admin@gmail.com",
        hashed_password=get_password_hash("admin")
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def auth_headers(client, test_user):
    """Get authentication headers."""
    from urllib.parse import urlencode

    response = await client.post(
        "/auth/login",
        data=urlencode({
            "username": "admin@gmail.com",
            "password": "admin"
        }),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    # Debug: print response if login fails
    if response.status_code != 200:
        print(f"Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        raise Exception(f"Login failed with status {response.status_code}")

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def test_book(db_session, test_user):
    """Create a test book."""
    book = Book(
        title="Test Book",
        author="Test Author",
        genre="Fiction",
        year_published=2024,
        summary="A test book",
    )
    db_session.add(book)
    await db_session.commit()
    await db_session.refresh(book)
    return book