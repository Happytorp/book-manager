from typing import Optional
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.models import Book, Review
from app.schemas.schemas import ReviewCreate
from app.services import book_services
from app.services.ai_service import generate_text


async def add_review(book_id: int, review_data: ReviewCreate, current_user, db: AsyncSession):
    """Add a review for a specific book."""
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    if not book:
        return None  # Book not found

    new_review = Review(
        book_id=book_id,
        user_id=current_user.id,
        review_text=review_data.review_text,
        rating=review_data.rating
    )
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    return new_review


async def get_reviews(book_id: int, db: AsyncSession):
    """Retrieve all reviews for a specific book."""
    result = await db.execute(select(Review).where(Review.book_id == book_id))
    return result.scalars().all()


async def aggregated_rating(db: AsyncSession, book_id: int) -> Optional[float]:
    """Calculate the average rating for a specific book."""
    q = select(func.avg(Review.rating)).where(Review.book_id == book_id)
    resp = await db.execute(q)
    avg_rating = resp.scalar_one_or_none()
    return float(avg_rating) if avg_rating is not None else None


async def get_book_summary(book_id: int, db: AsyncSession):
    """Get AI-generated summary of reviews and aggregated rating for a specific book."""
    # Fetch book
    book = await book_services.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # aggregated rating
    avg = await aggregated_rating(db, book_id)
    # generate review summary using llama from reviews text
    reviews = await get_reviews(book_id, db)
    review_texts = "\n\n".join(r.review_text for r in reviews)
    review_summary = None
    if review_texts.strip():
        prompt = f"Summarize these reviews into a concise summary and mention common pros and cons:\n\n{review_texts}\n\nSummary:"
        review_summary = await generate_text(prompt, max_tokens=200)
    return {
        "book_id": book.id,
        "title": book.title,
        "summary": book.summary,
        "average_rating": avg,
        "review_summary": review_summary,
    }
