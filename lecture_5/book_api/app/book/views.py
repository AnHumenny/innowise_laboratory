from typing import Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from lecture_5.book_api.app.book.models import Book
from lecture_5.book_api.app.book.schemas import BookItemCreate, BookItemUpdate
from lecture_5.book_api.app.book.services import get_books, create_book, remove_book, update_book_in_db, \
    search_books_in_db


async def list_items_view(db: AsyncSession, page: int, limit: int):
    """Responsible for handling request/response,
    delegating DB logic to service layer.
    """

    return await get_books(db, page, limit)


async def add_item_view(db: AsyncSession, item: BookItemCreate) -> Book:
    """Handles request for creating a new book.

    Delegates to the service layer and returns the created Book instance.
    """

    return await create_book(db, item)


async def remove_item_view(db: AsyncSession, item_id: int) -> dict:
    """Handles request to remove a book by ID.

    Delegates deletion to the service layer.

    Args:
        db (AsyncSession): Database session.
        item_id (int): ID of the book to remove.

    Returns:
        dict: Confirmation message upon successful deletion.
    """

    return await remove_book(db, item_id)


async def update_book_view(db: AsyncSession, book_id: int, item: BookItemUpdate) -> Any:
    """Handles updating an existing book.

    Delegates actual update logic to the service layer.

    Args:
        db (AsyncSession): Database session.
        book_id (int): ID of the book to update.
        item (BookItemUpdate): Fields to update.

    Returns:
        The updated book model instance.
    """

    return await update_book_in_db(db, book_id, item)

async def search_books_view(
    db: AsyncSession,
    page: int,
    limit: int,
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None
) -> List[Book]:
    """Handles searching for books with optional filters.

    Delegates actual search logic to the service layer.

    Args:
        db (AsyncSession): Database session.
        page (int): Page number (1-based index).
        limit (int): Number of items per page.
        title (Optional[str]): Filter by title (substring, case-insensitive).
        author (Optional[str]): Filter by author (substring, case-insensitive).
        year (Optional[int]): Filter by exact publication year.

    Returns:
        List[Book]: List of books matching the search criteria.
    """

    return await search_books_in_db(db, page, limit, title, author, year)
