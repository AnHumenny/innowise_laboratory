# Book API — FastAPI CRUD-a book management application

## Project Description

This project is a FastAPI learning application that implements a full set of CRUD operations
for the Book entity. The application allows you to create books,
get a list and individual entries, update data, delete books,
search by name and work with pagination. 

After the first launch, 
the application checks for the database and, if it is missing,
creates it by filling in test data or skips the creation step if available.

The project is built on an asynchronous stack:
**FastAPI + SQLAlchemy Async + SQLite + Pydantic**
and contains integration tests.

***

*Dockerfile*

The Dockerfile in lecture_6/ is used for building the Docker image. It installs Python dependencies
from requirements.txt, adds curl for internal testing (e.g., healthcheck queries),
sets the working directory to /app, copies the project code, initializes the database (via init_db.py), 
exposes port 8000, and launches the Uvicorn server with hot-reload enabled.
The file ensures the container is lightweight (based on python:3.12-slim)
and self-contained for the FastAPI app.

A HEALTHCHECK has been added to the Dockerfile using curl
to automatically check endpoint/healthcheck availability.

***
## API Features

### Creating a book
`POST /books/add`

### Getting a list of all books
`GET /books/`  

### Supports pagination:  
`GET /books/?page=1&limit=10`

### Getting a book by ID
`GET /books/{id}`

### Updating book data
`PUT /books/{id}`

### Deleting a book
`DELETE /books/remove/{id}`

### Search for books by name
`GET /books/search?title=Python`

## Technologies
- Python 3.12+
- FastAPI
- Uvicorn
- SQLAlchemy 2.0 (Async)
- Pydantic v2
- SQLite
- Pytest
- Asyncio

## Project structure
```
lecture_5/
│
└── book_api/
    │
    ├── app/
    │   ├── book/
    │   │   ├── tests/
    │   │   │   ├── __init__.py
    │   │   │   ├── conftest.py
    │   │   │   └── test_routes.py
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   ├── routes.py
    │   │   ├── schemas.py
    │   │   ├── services.py
    │   │   └── views.py
    │   │
    │   ├── core/
    │   │   ├── log/*.log
    │   │   │   ├── app.log
    │   │   │   ├── test.run.log
    │   │   │   └── test_log.py
    │   │   ├── test_log.py
    │   │   └── utils.py
    │   │
    │   ├── repository/
    │   │   ├── __init__.py
    │   │   ├── database.py
    │   │   ├── DB.db
    │   │   └── init_db.py
    │   │
    │   ├── __init__.py
    │   └── main.py
    │
    ├── __init__.py
    ├── .dockerignore
    ├── Dockerfile
    └── ReadMe.md
    
```

## Launching the app

### 1. Installing
pip install -r dependencies requirements.txt


### 2. Launch
uvicorn lecture_5.book_api.main:app --reload


### 3. Swagger UI
After launching, the API is available here:  
http://localhost:8000/docs


## Testing
The project contains API integration tests.


### Running all tests:
pytest -v -s


### Running a specific test file:
pytest lecture_5/book_api/app/books/tests/test_routes.py -v -s


## Environment Settings
The database is configured in `repository/database.py`.  
SQLite is used by default. At the first launch, the existence of the database is checked and, 
if it does not exist, it is created and filled with test data.


## Notes
- The tests use a temporary test database that is created before launch and deleted after.
- The service layer is completely separate from the routes.
- The API strictly validates data via Pydantic.
