import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.schemas import ReviewCreate, ReviewOut
from app.services.review_services import get_reviews, get_book_summary, add_review
from app.api.routers.auth import get_current_user
from app.models.models import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/{book_id}/reviews", response_model=ReviewOut)
async def create_review(book_id: int, review: ReviewCreate, current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    """Add a review for a specific book."""
    result = await add_review(book_id, review, current_user, db)
    logger.info(f"User {current_user.email} added a review for book ID {book_id}")
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return result


@router.get("/{book_id}/reviews", response_model=List[ReviewOut])
async def list_reviews(book_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve all reviews for a specific book."""
    logger.info(f"Retrieving reviews for book ID {book_id}")
    return await get_reviews(book_id, db)


@router.get("/{book_id}/summary")
async def book_summary(book_id: int, db: AsyncSession = Depends(get_db)):
    """Get AI-generated summary of reviews and aggregated rating for a specific book."""
    summary = await get_book_summary(book_id, db)
    logger.info(f"Retrieving AI-generated summary for book ID {book_id}")
    if summary is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return summary
