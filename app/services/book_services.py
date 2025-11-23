from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import logging

from app.models.models import Book
from app.schemas.schemas import BookCreate
from app.utility.redis_client import cache_get, cache_set, cache_delete

logger = logging.getLogger(__name__)


async def create_book(db: AsyncSession, data: BookCreate) -> Book:
    """Create a book with basic information (legacy function)."""
    book = Book(**data.model_dump())
    db.add(book)
    await db.commit()
    await db.refresh(book)
    await cache_delete("books:all")
    return book


async def get_all_books(db: AsyncSession):

    """Retrieve all books from the database."""
    cache_key = "books:all"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    result = await db.execute(select(Book))
    books = result.scalars().all()
    await cache_set(cache_key, [book.to_dict() for book in books])
    return books


async def get_book_by_id(db: AsyncSession, book_id: int):
    """Retrieve a book by ID."""
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()


async def update_book(db: AsyncSession, book_id: int, data: BookCreate) -> Optional[Book]:
    """Update a book by ID."""
    book = await get_book_by_id(db, book_id)
    if not book:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(book, key, value)

    db.add(book)
    await db.commit()
    await db.refresh(book)
    await cache_delete("books:all")
    return book


async def delete_book(db: AsyncSession, book_id: int) -> Optional[Book]:
    """Delete a book by ID."""
    book = await get_book_by_id(db, book_id)
    if not book:
        return None

    await db.delete(book)
    await db.commit()
    await cache_delete("books:all")
    return book

