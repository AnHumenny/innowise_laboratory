import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../../.."))
sys.path.insert(0, project_root)

try:
    from lecture_5.book_api.main import app
    from lecture_5.book_api.app.book.models import Base, Book
    print("Imported app and models")
except ImportError as e:
    raise ImportError(f"Cannot import app/models: {e}")

TEST_DATABASE_URL = "sqlite:///./test_books.db"

@pytest.fixture(scope="session")
def engine():
    """A fixture for the database engine."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)

    Base.metadata.create_all(bind=engine)
    print("Created database tables")

    yield engine

    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test_books.db"):
        os.remove("test_books.db")
    print("Dropped database tables and deleted test DB file")


@pytest.fixture
def db_session(engine):
    """The fixture for the DB session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client():
    """A fixture for the FastAPI test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_database(db_session):
    """Automatically clears the Book table after each test."""
    yield

    try:
        db_session.query(Book).delete()
        db_session.commit()
        print(" : Database cleaned after test")

    except Exception as e:
        db_session.rollback()
        print(f"Could not clean database: {e}")
