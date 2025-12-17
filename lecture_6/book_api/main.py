import sys
from pathlib import Path
from .repository.init_db import init_database
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.responses import HTMLResponse
from .app.book.routes import router as book_router

current_file = Path(__file__).resolve()
book_api_root = current_file.parent
if str(book_api_root) not in sys.path:
    sys.path.insert(0, str(book_api_root))

@asynccontextmanager
async def lifespan(_: FastAPI):
    """Asynchronous context manager for the FastAPI application lifecycle.

    Performs database initialization at application startup using
    the init_database function from the init_db module. After initialization,
    control is transferred to FastAPI for request processing.

    Tables are created only if they do not already exist in the database.

    Note: The database initialization step can be removed or commented out
    after the first successful launch to avoid redundant table creation.

    Args:
        _: An instance of the FastAPI application (automatically passed by FastAPI,
            but not directly used in this lifespan function).

    Yields:
        None: Transfers control to the application after initialization.
    """
    await init_database()
    yield


app = FastAPI(title="Book API -- FastAPI CRUD - a book management application",
              version="1.0.0", lifespan=lifespan)

app.include_router(book_router, prefix="/books", tags=["books"])


@app.get("/")
async def start_page():
    """Root endpoint to verify that the FastAPI application is running.

    Returns:
        HTMLResponse: An HTML message confirming that the application is running,
                      including a link to `/docs` for API documentation.
    """
    html_content = ("<div align=center><h4>Hello FastAPI with a book management application!"
                    "<br><a href='/docs'>Go to the page documentation</a></h4></div>")
    return HTMLResponse(content=html_content)


@app.get("/healthcheck")
async def healthcheck() -> dict:
    """Health check endpoint to verify the API is running.

    Returns:
        dict: A dictionary containing the status of the API.
           Example: {"status": "ok"}
    """

    return {"status": "ok"}
