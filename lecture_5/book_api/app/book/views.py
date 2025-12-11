from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from lecture_5.book_api.app.book.models import Book
from lecture_5.book_api.app.book.schemas import BookItemCreate, BookItemUpdate, MessageResponse, BookItemRead
from lecture_5.book_api.app.book.services import get_books, create_book, search_books_in_db, update_book_in_db, \
    remove_book, get_book_in_db


async def list_items_view(db: AsyncSession, page: int, limit: int):
    """Responsible for handling request/response, delegating DB logic to service layer."""

    return await get_books(db, page, limit)


async def add_item_view(db: AsyncSession, item: BookItemCreate) -> Book:
    """Handles request for creating a new book.

    Delegates to the service layer and returns the created Book instance.
    """

    return await create_book(db, item)


async def remove_item_view(db: AsyncSession, item_id: int) -> MessageResponse:
    """Delete a book by its ID and return a confirmation message.

    Delegates all database work to the `remove_book` function.
    """
    result = await remove_book(db, item_id)
    return MessageResponse(message=result["message"])


async def update_book_view(
    db: AsyncSession,
    book_id: int,
    item: BookItemUpdate
) -> BookItemRead:
    """Update a book by its ID and return the updated record.

    Args:
        db (AsyncSession): Active SQLAlchemy async session.
        book_id (int): ID of the book to update.
        item (BookItemUpdate): Pydantic model with fields to update.

    Raises:
        HTTPException: If the book with the given ID does not exist (404).

    Returns:
        BookItemRead: Updated book record as a Pydantic model.
    """
    book = await update_book_in_db(db, book_id, item)
    return BookItemRead.model_validate(book)


async def search_books_view(
    db: AsyncSession,
    page: int = 1,
    limit: int = 10,
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None
) -> List[BookItemRead]:
    """Search for books using optional filters and pagination."""
    books = await search_books_in_db(db, page, limit, title, author, year)
    return [BookItemRead.model_validate(book) for book in books]


async def get_book_view(db: AsyncSession, book_id: int) -> BookItemRead:
    """Return a single book by its ID."""
    book = await get_book_in_db(db, book_id)
    return BookItemRead.model_validate(book)
