import asyncio
from pathlib import Path
from lecture_5.book_api.core.utils import logger
from lecture_5.book_api.repository.database import engine, async_session, DB_BOOK
from lecture_5.book_api.app.book.models import Book as Book_create

DB_FILE = Path(__file__).parent / DB_BOOK

async def init_database():
    """Asynchronous database initialization.

    Checks if the SQLite database file exists. If there is no file:
        - creates a database file,
        - creates all tables defined in Base.metadata,
        - displays a message about the creation and initialization of the database.

    If the database already exists, the function does not change anything and outputs
    a message about skipping creation.

    It is used for the safe start of FastAPI applications or others.
    asynchronous tasks with the database.
    """
    test_books = [
        {"title": "Clean Code", "author": "Robert C. Martin", "year": 2008},
        {"title": "The Pragmatic Programmer", "author": "Andrew Hunt", "year": 1999},
        {"title": "Design Patterns", "author": "Erich Gamma", "year": 1994},
        {"title": "Refactoring", "author": "Martin Fowler", "year": 1999},
        {"title": "Code Complete", "author": "Steve McConnell", "year": None},
        {"title": "Effective Java", "author": "Joshua Bloch", "year": 2001},
        {"title": "Python Tricks", "author": "Dan Bader", "year": 2017},
        {"title": "Deep Work", "author": "Cal Newport", "year": 2016},
        {"title": "The Clean Coder", "author": "Robert C. Martin", "year": None},
        {"title": "Working Effectively with Legacy Code", "author": "Michael Feathers", "year": 2004},
    ]

    if not DB_FILE.exists():
        async with engine.begin() as conn:
            await conn.run_sync(Book_create.metadata.create_all)
            async with async_session() as session:
                async with session.begin():
                    for b in test_books:
                        book = Book_create(title=b["title"], author=b["author"], year=b["year"])
                        session.add(book)
                await session.commit()
                logger.info("10 test books added to database!")
        logger.info("Database created and initialized with tables and 10 test books added to database!")
    else:
        logger.warning("Database already exists, skipping creation.")


if __name__ == "__main__":
    asyncio.run(init_database())
