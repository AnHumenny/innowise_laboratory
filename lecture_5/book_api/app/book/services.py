import traceback
from sqlite3 import IntegrityError
from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy import select, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Book
from .schemas import BookItemCreate, BookItemUpdate
from ...core.utils import logger


async def get_books(db: AsyncSession, page: int, limit: int) -> list[Book]:
    """Fetch paginated books from the database.

    Uses SQL LIMIT/OFFSET to return only a portion of records.

    Args:
        db (AsyncSession): Database session.
        page (int): Current page number (1-based).
        limit (int): Number of items per page.

    Returns:
        list[Book]: Books for the requested page.

    Raises:
        HTTPException: If a database error occurs.
    """
    offset = (page - 1) * limit

    try:
        result = await db.execute(
            select(Book).offset(offset).limit(limit)
        )

        return list(result.scalars().all())

    except SQLAlchemyError as e:
        logger.error("Database transaction rolled back in book get "
                     "due to an error:\n%s", traceback.format_exc())

        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def create_book(db: AsyncSession, item: BookItemCreate) -> Book:
    """Create a new book record in the database.

    Args:
        db (AsyncSession): Active database session.
        item (BookItemCreate): Incoming book data.

    Returns:
        Book: Persisted SQLAlchemy model instance.

    Raises:
        HTTPException: If a database error occurs during the query.
                       The transaction is rolled back in this case.
    """
    book = Book(title=item.title, author=item.author, year=item.year)

    db.add(book)

    try:
        await db.commit()
        await db.refresh(book)

    except IntegrityError as e:
        await db.rollback()
        logger.error("Database error occurred in books create_book:\n%s", traceback.format_exc())

        raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")

    except SQLAlchemyError as e:
        logger.error("Database transaction rolled back in book create_book "
                     "due to an error:\n%s", traceback.format_exc())

        await db.rollback()

        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return book


async def remove_book(db: AsyncSession, book_id: int) -> dict:
    """Remove a book by its ID from the database.

    Args:
        db (AsyncSession): Active SQLAlchemy asynchronous session.
        book_id (int): ID of the book to delete.

    Returns:
        dict: A confirmation message indicating successful deletion.

    Raises:
        HTTPException:
            - 404: If no book with the specified ID exists.
            - 500: If a database error occurs (transaction is rolled back on error).
    """
    try:
        result = await db.execute(select(Book).where(Book.id == book_id))
        item = result.scalars().first()

        if not item:
            logger.error("Database error occurred in books remove_book:\n%s", traceback.format_exc())
            raise HTTPException(status_code=404, detail="Item not found")

        await db.delete(item)
        await db.commit()

        return {"message": f"Item {book_id} removed from database"}

    except SQLAlchemyError as e:
        logger.error("Database transaction rolled back in book remove_book "
                     "due to an error:\n%s", traceback.format_exc())

        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def update_book_in_db(db: AsyncSession, book_id: int, item: BookItemUpdate) -> Book:
    """Update an existing book in the database.

    Supports partial updates: only fields provided in `item` are modified.

    Args:
        db (AsyncSession): Active SQLAlchemy asynchronous session.
        book_id (int): ID of the book to update.
        item (BookItemUpdate): Pydantic model containing fields to update.

    Returns:
        Book: The updated SQLAlchemy model instance.

    Raises:
        HTTPException:
            - 404: If no book with the specified ID exists.
            - 500: If a database error occurs (transaction is rolled back on error).
    """
    try:
        result = await db.execute(select(Book).where(Book.id == book_id))
        book = result.scalars().first()

        if not book:
            logger.error("Database error occurred in books update_book_in_db:\n%s", traceback.format_exc())
            raise HTTPException(status_code=404, detail="Book not found")

        for field, value in item.model_dump(exclude_unset=True).items():
            setattr(book, field, value)

        db.add(book)

        await db.commit()
        await db.refresh(book)
        return book

    except SQLAlchemyError as e:
        logger.error("Database transaction rolled back in book update_book_in_db "
                     "due to an error:\n%s", traceback.format_exc())

        await db.rollback()

        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def search_books_in_db(db: AsyncSession, page: int, limit: int, title: Optional[str] = None,
                             author: Optional[str] = None, year: Optional[int] = None
                             ) -> List[Book]:
    """Search for books using multiple optional filters.

    Performs partial matching for `title` and `author`.
    All provided filters are combined using OR logic.
    If no filters are provided, returns an empty list.

    Args:
        db (AsyncSession): Active SQLAlchemy asynchronous session.
        page (int): Current page number (1-based).
        limit (int): Number of items per page.
        title (Optional[str]): Filter by title (substring, case-insensitive).
        author (Optional[str]): Filter by author (substring, case-insensitive).
        year (Optional[int]): Filter by exact publication year.

    Returns:
        List[Book]: List of books matching the search criteria.

    Raises:
        HTTPException:
            - 500: If a database error occurs (transaction rollback performed).
    """
    try:
        offset = (page - 1) * limit
        filters = []

        if title:
            filters.append(Book.title.ilike(f"%{title}%"))
        if author:
            filters.append(Book.author.ilike(f"%{author}%"))
        if year:
            filters.append(Book.year == year)

        if not filters:
            return []

        query = select(Book).where(or_(*filters)).offset(offset).limit(limit)
        result = await db.execute(query)
        books: List[Book] = result.scalars().all()          # type: ignore[list-item]
        return books

    except SQLAlchemyError as e:
        logger.error("Database transaction rolled back in book search_books_in_db "
                     "due to an error:\n%s", traceback.format_exc())

        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
