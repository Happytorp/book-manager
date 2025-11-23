from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
import logging

from app.db.base import Base
from app.api.routers.books import router as books_router
from app.api.routers.reviews_router import router as reviews_router
from app.api.routers.auth import router as auth_router
from app.config import settings
from app.models.models import Book
from app.db.session import get_db
from app.services.ai_service import summarize_text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_db():
    """Initialize database tables."""
    engine = create_async_engine(settings.DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        # Drop all tables (optional, for development)
        # await conn.run_sync(Base.metadata.drop_all)

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables verified/created successfully")

    await engine.dispose()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ----------------- STARTUP -----------------
    logger.info("Starting Book Manager API with lifespan...")
    # Init database
    await init_db()
    logger.info("Book Manager API started successfully")
    # Yield control to the application
    yield
    # ----------------- SHUTDOWN -----------------
    logger.info("Shutting down Book Manager API...")
    logger.info("Shutdown complete.")


app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent book management system with AI-powered summaries and recommendations",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Create a separate router for root-level endpoints
root_router = APIRouter()


@app.get("/recommendations")
async def recommendations(genre: str = None, author: str = None, limit: int = 10,
                          session: AsyncSession = Depends(get_db)):
    """Get book recommendations based on user preferences."""
    q = select(Book)
    if genre:
        q = q.where(Book.genre == genre)
    if author:
        q = q.where(Book.author == author)
    q = q.limit(limit)
    resp = await session.execute(q)
    books = resp.scalars().all()
    return books


@app.post("/generate-summary")
async def generate_summary(content: dict):
    """Generate a summary for a given book content."""
    text = content.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Missing 'text' in payload")
    summary = await summarize_text(text)
    return {"summary": summary}


# Include the routers
app.include_router(root_router)
app.include_router(books_router, prefix="/books", tags=["Books"])
app.include_router(reviews_router, prefix="/books", tags=["Reviews"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/health_check")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
