import pytest
from ....core.test_log import test_logger


@pytest.fixture
def created_book_id(client) -> int:
    """Automatically clears the Book table after each test."""

    book_data = {
        "title": "API Test Book",
        "author": "API Test Author",
        "year": 2024,
        "description": "Created via fixture"
    }

    response = client.post("/books/add", json=book_data)
    assert response.status_code in [200, 201]

    book_id = response.json()["id"]
    test_logger.info(f"Fixture: Created book with ID: {book_id}")
    test_logger.info(f"Fixture: Response JSON: {response.json()}")
    test_logger.info(f"Fixture: Response status: {response.status_code}")

    return book_id


def test_list_books_api(client):
    """API test: GET /books/ - getting a list of books."""

    test_name = "test_list_books_api"
    test_logger.info(f"Starting test: {test_name}")

    response = client.get("/books/")
    test_logger.info(f"{test_name}: GET /books/ -> {response.status_code}")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    test_logger.info(f"{test_name}: Response contains {len(data)} books")

    if data:
        sample = data[0]
        test_logger.info(f"{test_name}: Sample books fields: {list(sample.keys())}")

    test_logger.info(f"Test passed: {test_name}")


def test_create_book_api(client):
    """API test: POST /books/add - create a book through the API."""

    test_name = "test_create_book_api"
    test_logger.info(f"Starting test: {test_name}")

    book_data = {
        "title": "API Test Book",
        "author": "API Test Author",
        "year": 2024,
        "description": "Created via API test"
    }

    response = client.post("/books/add", json=book_data)
    test_logger.info(f"{test_name}: POST /books/add -> {response.status_code}")

    assert response.status_code in [200, 201]

    data = response.json()
    assert "id" in data
    assert data["title"] == book_data["title"]

    test_logger.info(f"{test_name}: Created book with id={data['id']}")
    test_logger.info(f"Test passed: {test_name}")


def test_create_book_api_validation(client):
    """API test: validation of data when creating a book."""

    test_name = "test_create_book_api_validation"
    test_logger.info(f"Starting test: {test_name}")

    invalid_data = {"author": "Author Only"}
    response = client.post("/books/add", json=invalid_data)
    test_logger.info(f"{test_name}: POST /books/add (invalid) -> {response.status_code}")

    assert response.status_code == 422

    error_detail = response.json()['detail']
    test_logger.info(f"{test_name}: Validation error: {error_detail}")
    test_logger.info(f"Test passed: {test_name}")


def test_get_book_api(client, created_book_id):
    """API test: GET /books/{id} - getting one book."""

    test_name = "test_get_book_api"
    test_logger.info(f"Starting test: {test_name}")

    response = client.get(f"/books/{created_book_id}")
    test_logger.info(f"{test_name}: GET /books/{created_book_id} -> {response.status_code}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == created_book_id

    test_logger.info(f"{test_name}: Retrieved book: {data['title']}")
    test_logger.info(f"Test passed: {test_name}")


def test_update_book_api(client, created_book_id):
    """API test: PUT /books/{id} - updating the book."""

    test_name = "test_update_book_api"
    test_logger.info(f"Starting test: {test_name}")

    update_data = {
        "title": "API Updated Title",
        "author": "API Updated Author",
        "year": 2025
    }

    test_logger.info(f"{test_name}: Update data: {update_data}")

    response = client.put(f"/books/{created_book_id}", json=update_data)
    test_logger.info(f"{test_name}: PUT /books/{created_book_id} -> {response.status_code}")

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == update_data["title"]

    test_logger.info(f"{test_name}: Updated book: {data['title']}")
    test_logger.info(f"Test passed: {test_name}")


def test_delete_book_api(client, created_book_id):
    """API test: DELETE /books/remove/{id} - deleting a book."""

    test_name = "test_delete_book_api"
    test_logger.info(f"Starting test: {test_name}")

    response = client.delete(f"/books/remove/{created_book_id}")
    test_logger.info(f"{test_name}: DELETE /books/remove/{created_book_id} -> {response.status_code}")

    assert response.status_code == 200

    data = response.json()
    assert "message" in data

    test_logger.info(f"{test_name}: Delete response: {data['message']}")

    get_response = client.get(f"/books/{created_book_id}")
    test_logger.info(f"{test_name}: GET after DELETE -> {get_response.status_code}")
    assert get_response.status_code == 404

    test_logger.info(f"Test passed: {test_name}")


def test_search_books_api(client):
    """API test: GET /books/search - book search."""

    test_name = "test_search_books_api"
    test_logger.info(f"Starting test: {test_name}")

    test_books = [
        {"title": "Python API Testing", "author": "Developer One", "year": 2023},
        {"title": "FastAPI Guide", "author": "Developer Two", "year": 2022},
    ]

    created_ids = []
    for book in test_books:
        response = client.post("/books/add", json=book)
        book_id = response.json()["id"]
        created_ids.append(book_id)
        test_logger.info(f"{test_name}: Created test book: {book['title']} (id={book_id})")

    response = client.get("/books/search?title=Python")
    test_logger.info(f"{test_name}: GET /books/search?title=Python -> {response.status_code}")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    test_logger.info(f"{test_name}: Found {len(data)} books with 'Python'")

    for book_id in created_ids:
        client.delete(f"/books/remove/{book_id}")

    test_logger.info(f"Test passed: {test_name}")


def test_api_pagination(client):
    """API test: pagination in GET /book/."""

    test_name = "test_api_pagination"
    test_logger.info(f"Starting test: {test_name}")

    response = client.get("/books/?page=1&limit=3")
    test_logger.info(f"{test_name}: GET /books/?page=1&limit=3 -> {response.status_code}")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    test_logger.info(f"{test_name}: Page 1 with limit 3: {len(data)} books")
    test_logger.info(f"Test passed: {test_name}")
