import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.schemas import BookCreate, BookOut
from app.services.book_services import (
    create_book,
    get_book_by_id,
    update_book,
    delete_book
)
from app.api.routers.auth import get_current_user
from app.db.session import get_db
from app.services.ai_service import summarize_text
from app.services.book_services import get_all_books

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(get_current_user)])


# POST /books - add a new book
@router.post("/", response_model=BookOut)
async def add_book(book_data: BookCreate, db: AsyncSession = Depends(get_db)):
    """Create a new book entry (basic version without AI summary)."""
    book = await create_book(db, book_data)
    logger.info(f"Book '{book.title}' by {book.author} created with ID {book.id}")
    if not book.summary:
        # call llama to generate summary based on title+author (or full content if provided)
        prompt = f"Write a short summary for the book titled '{book.title}' by {book.author}."
        summary = await summarize_text(prompt)
        book.summary = summary
        db.add(book)
        await db.commit()
        await db.refresh(book)
    return book


# GET /books - retrieve all books
@router.get("/", response_model=list[BookOut])
async def list_books(db: AsyncSession = Depends(get_db)):
    """Retrieve all books from the database."""
    books = await get_all_books(db)
    logger.info(f"Retrieved {len(books)} books from the database")
    return books


# GET /books/{id} - retrieve a specific book by its ID
@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a specific book by its ID."""
    book = await get_book_by_id(db, book_id)
    logger.info(f"Retrieved book with ID {book_id}")
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# PUT /books/{id} - update a book's information by its ID
@router.put("/{book_id}", response_model=BookOut)
async def update_book_endpoint(book_id: int, book_data: BookCreate, db: AsyncSession = Depends(get_db)):
    """Update a book's information by its ID."""
    updated_book = await update_book(db, book_id, book_data)
    logger.info(f"Updated book with ID {book_id}")
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


# DELETE /books/{id} - delete a book by its ID
@router.delete("/{book_id}", response_model=BookOut)
async def delete_book_endpoint(book_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a book by its ID."""
    deleted_book = await delete_book(db, book_id)
    logger.info(f"Deleted book with ID {book_id}")
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book
