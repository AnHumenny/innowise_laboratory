from typing import List, Optional, Any
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Book
from .schemas import BookItemCreate, BookItemRead, BookItemUpdate
from .views import list_items_view, add_item_view, remove_item_view, update_book_view, search_books_view
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
        db: AsyncSession = Depends(get_db)
):
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
    "/add",
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
async def add_item(item: BookItemCreate, db: AsyncSession = Depends(get_db)) -> Any:
    """Create a new book record and return it."""

    return await add_item_view(db, item)


@router.delete(
    "/remove/{item_id}",
    summary="Delete a book by ID",
    description="""
        **Delete a book by its ID.**

        - **item_id**: int — ID of the book to delete

        Returns a confirmation message if the deletion is successful.
        Raises a 404 error if the book does not exist.
    """,
    responses={
        200: {"description": "Book successfully removed"},
        404: {"description": "Book not found"},
        500: {"description": "Database error occurred"},
    },
)
async def remove_item(item_id: int, db: AsyncSession = Depends(get_db)) -> Any:
    """Endpoint to delete a book by ID.

    Delegates the operation to the views layer.
    """
    return await remove_item_view(db, item_id)


@router.put(
    "/{book_id}",
    response_model=BookItemRead,
    summary="Update an existing book",
    description="""
            Update an existing book record by its ID.

            Only the fields provided in the request are updated (partial update).
            To set a field to NULL, explicitly pass `null` for that field.

            **Request body:**
            - title: str (optional) — If provided, updates the title
            - author: str (optional) — If provided, updates the author  
            - year: int | null (optional) — If provided, updates the year. 
                       Pass `null` to clear the year field.

            **Path parameter:**
            - book_id: int — ID of the book to update

            **Returns:** Updated book record
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
):
    return await update_book_view(db, book_id, item)


@router.get(
    "/search",
    response_model=List[BookItemRead],
    summary="Search books with optional filters",
    description="""
        Search for books by optional filters: title, author, and year.

        **Query parameters:**
        - page: int — Page number (starting from 1)
        - limit: int — Number of items per page
        - title: str (optional) — Search by title substring
        - author: str (optional) — Search by author substring
        - year: int (optional) — Search by exact year

        **Returns:** List of books matching the search criteria
    """,
    responses={
        200: {"description": "List of books matching the search criteria"},
        500: {"description": "Database error occurred"}
    }
)
async def search_books(
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    title: Optional[str] = Query(None, description="Search by title"),
    author: Optional[str] = Query(None, description="Search by author"),
    year: Optional[int] = Query(None, description="Search by year"),
    db: AsyncSession = Depends(get_db)
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
        List[BookItemRead]: A list of books matching the search criteria.
    """

    return await search_books_view(db, page, limit, title, author, year)


@router.get(
    "/{book_id}",
    response_model=BookItemRead,
    summary="Get book by ID",
    responses={
        200: {"description": "Book found"},
        404: {"description": "Book not found"},
    },
)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a single book by ID (using for tests)."""

    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book
