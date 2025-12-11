from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Book
from .schemas import BookItemCreate, BookItemRead, BookItemUpdate, MessageResponse
from .views import (list_items_view, add_item_view, remove_item_view, update_book_view,
                    search_books_view, get_book_view)
from ...repository.database import get_db

router = APIRouter()

@router.get(
    "/",
    response_model=List[BookItemRead],
    summary="Retrieve paginated list of books",
    description="""
        **Retrieve paginated list of books.**

        *Query parameters:*
        - **page**: int — Page number (starting from 1)
        - **limit**: int — Number of items per page

        *Returns:* List of books matching pagination.
    """,
    responses={
        200: {"description": "A list of books"},
        500: {"description": "Database error occurred"},
    },
)
async def list_items(
        page: int = Query(1, ge=1, description="Page number (starting from 1)"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
        db: AsyncSession = Depends(get_db),
) -> list[BookItemRead]:
    """Retrieve paginated list of books.

    Args:
        page (int): Which page to return (1-based index).
        limit (int): Number of items per page.
        db (AsyncSession): Database session.

    Returns:
        list[BookItemRead]: A portion of books based on pagination.
    """
    return await list_items_view(db, page, limit)


@router.post(
    "/",
    response_model=BookItemRead,
    status_code=201,
    summary="Add a new book",
    description="""
        **Create a new book entry.**

        Accepts the following data in request body:

        - **title**: str — Book title (required)
        - **author**: str — Book author (required)
        - **year**: int — Publication year (optional, pass `null` to clear)

        Returns the created book record.
    """,
)
async def add_item(
    item: BookItemCreate,
    db: AsyncSession = Depends(get_db),
) -> Book:
    """Create a new book record and return it.

    Args:
        item (BookItemCreate): Pydantic model containing data for the new book.
        db (AsyncSession): Active SQLAlchemy async session.

    Returns:
        BookItemRead: The newly created book as a Pydantic model.
    """
    return await add_item_view(db, item)


@router.delete(
    "/{book_id}",
    summary="Delete a book by ID",
    description="""
        **Delete a book by its ID.**

        - **book_id**: int — ID of the book to delete

        Returns a confirmation message if the deletion is successful.
        Raises a 404 error if the book does not exist.
    """,
    response_model=MessageResponse,
    responses={
    200: {"description": "Book successfully removed"},
    404: {"description": "Book not found"},
    500: {"description": "Database error occurred"},
    },
)
async def remove_item(book_id: int, db: AsyncSession = Depends(get_db)) -> MessageResponse:
    """Delete a book by its ID and return a confirmation message.

    Args:
        book_id (int): ID of the book to delete.
        db (AsyncSession): Active SQLAlchemy async session.

    Raises:
        HTTPException: If the book with the given ID does not exist (404).

    Returns:
        MessageResponse: Pydantic model containing a confirmation message.
                         Example: "Book successfully removed".
    """
    return await remove_item_view(db, book_id)


@router.put(
    "/{book_id}",
    response_model=BookItemRead,
    summary="Update an existing book",
    description="""
        Update an existing book record by its ID.

        - **book_id**: int — Unique identifier of the book to update.

        This endpoint performs a **partial update**:  
        only the fields provided in the request body will be updated.

        To explicitly clear a field, pass `null` for that field.

        Returns the updated book record.
    """,
    responses={
        200: {"description": "Book successfully updated"},
        404: {"description": "Book not found"},
        500: {"description": "Database error occurred"},
    },
)
async def update_book(
    book_id: int,
    item: BookItemUpdate,
    db: AsyncSession = Depends(get_db)
) -> BookItemRead:
    """Update an existing book by its ID and return the updated record.

    This endpoint performs a partial update: only the fields provided
    in the request are updated. To clear a field, explicitly pass `null`.

    Args:
        book_id (int): ID of the book to update.
        item (BookItemUpdate): Pydantic model containing fields to update.
        db (AsyncSession): Active SQLAlchemy async session.

    Raises:
        HTTPException: If the book with the given ID does not exist (404).

    Returns:
        BookItemRead: Updated book record as a Pydantic model.
    """
    return await update_book_view(db, book_id, item)


@router.get(
    "/search",
    response_model=List[BookItemRead],
    summary="Search books with optional filters",
    description="""
        Search books using optional filtering and pagination.

        You can filter the results by:
        - **title** — partial match by book title
        - **author** — partial match by author name
        - **year** — exact match by publication year

        Pagination is controlled using:
        - **page** — page number (starting from 1)
        - **limit** — number of items per page

        If no filters are provided, an empty list is returned.
    """
)
async def search_books(
    db: AsyncSession = Depends(get_db),
    page: int = 1,
    limit: int = 10,
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None
):
    """Search for books using optional filters and pagination.

    This endpoint allows searching books by title, author, and/or year.
    If no filters are provided, returns an empty list.
    Pagination is controlled via `page` and `limit` query parameters.

    Args:
        page (int, optional): Page number (starting from 1). Defaults to 1.
        limit (int, optional): Number of items per page. Defaults to 10.
        title (str | None, optional): Filter books by title substring. Defaults to None.
        author (str | None, optional): Filter books by author substring. Defaults to None.
        year (int | None, optional): Filter books by exact publication year. Defaults to None.
        db (AsyncSession): Active SQLAlchemy database session (injected by Depends on).

    Returns:
        List[BookItemRead]: A list of books matching the search criteria or [] if empty.
    """
    return await search_books_view(db, page, limit, title, author, year)


@router.get(
    "/{book_id}",
    response_model=BookItemRead,
    summary="Get book by ID",
    description="""
        Retrieve a single book by its unique identifier(using for tests).
    
        This endpoint returns full information about a book
        if a record with the specified **book_id** exists in the database.

        - **book_id**: int — ID of the book 
        If the book is not found, a **404 Not Found** error is returned.
    """,
    responses={
        200: {"description": "Book found"},
        404: {"description": "Book not found"},
    },
)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a single book by ID (using for tests)."""

    return await get_book_view(db, book_id)
