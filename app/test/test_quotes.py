from fastapi.testclient import TestClient


def test_get_random_quote(client: TestClient):
    """Test getting a random quote."""
    # Create a user and get a token
    client.post(
        "/users/",
        json={"username": "quoteuser_rand", "email": "quote_rand@example.com", "password": "password"},
    )
    login_response = client.post(
        "/token",
        data={"username": "quoteuser_rand", "password": "password"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # First create a quote
    client.post(
        "/quotes",
        headers=headers,
        json={"text": "This is a test quote for random.", "author": "Random Author"},
    )

    # Get random quote
    response = client.get("/quotes")
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "author" in data
    assert "id" in data


def test_read_all_quotes(client: TestClient):
    """Test reading all quotes."""
    response = client.get("/quotes/all")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_quote(client: TestClient):
    """Test creating a quote with authentication."""
    # Create a user and get a token
    client.post(
        "/users/",
        json={"username": "quoteuser", "email": "quote@example.com", "password": "password"},
    )
    login_response = client.post(
        "/token",
        data={"username": "quoteuser", "password": "password"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a quote
    response = client.post(
        "/quotes",
        headers=headers,
        json={"text": "This is a test quote.", "author": "Test Author"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "This is a test quote."
    assert data["author"] == "Test Author"
    assert "id" in data


def test_create_quote_with_category(client: TestClient):
    """Test creating a quote with a category."""
    # Create a user and get a token
    client.post(
        "/users/",
        json={"username": "quoteuser_cat", "email": "quote_cat@example.com", "password": "password"},
    )
    login_response = client.post(
        "/token",
        data={"username": "quoteuser_cat", "password": "password"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a quote with category
    response = client.post(
        "/quotes",
        headers=headers,
        json={"text": "A quote with category.", "author": "Test Author", "category": "Philosophy"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["category"] == "Philosophy"


def test_create_quote_default_category(client: TestClient):
    """Test that quotes have 'General' as default category."""
    # Create a user and get a token
    client.post(
        "/users/",
        json={"username": "quoteuser_def", "email": "quote_def@example.com", "password": "password"},
    )
    login_response = client.post(
        "/token",
        data={"username": "quoteuser_def", "password": "password"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a quote without category
    response = client.post(
        "/quotes",
        headers=headers,
        json={"text": "A quote without explicit category.", "author": "Test Author"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["category"] == "General"


def test_create_quote_unauthenticated(client: TestClient):
    """Test that creating a quote without authentication fails."""
    response = client.post(
        "/quotes",
        json={"text": "This is a test quote.", "author": "Test Author"},
    )
    assert response.status_code == 401


def test_create_quote_text_too_short(client: TestClient):
    """Test that creating a quote with text less than 10 characters fails."""
    # Create a user and get a token
    client.post(
        "/users/",
        json={"username": "quoteuser_short", "email": "quote_short@example.com", "password": "password"},
    )
    login_response = client.post(
        "/token",
        data={"username": "quoteuser_short", "password": "password"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/quotes",
        headers=headers,
        json={"text": "Short", "author": "Test Author"},
    )
    assert response.status_code == 422


def test_create_quote_author_too_short(client: TestClient):
    """Test that creating a quote with author less than 3 characters fails."""
    # Create a user and get a token
    client.post(
        "/users/",
        json={"username": "quoteuser_auth", "email": "quote_auth@example.com", "password": "password"},
    )
    login_response = client.post(
        "/token",
        data={"username": "quoteuser_auth", "password": "password"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/quotes",
        headers=headers,
        json={"text": "This is a valid quote text.", "author": "AB"},
    )
    assert response.status_code == 422


def test_create_quote_missing_fields(client: TestClient):
    """Test that creating a quote with missing required fields fails."""
    # Create a user and get a token
    client.post(
        "/users/",
        json={"username": "quoteuser_miss", "email": "quote_miss@example.com", "password": "password"},
    )
    login_response = client.post(
        "/token",
        data={"username": "quoteuser_miss", "password": "password"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Missing author
    response = client.post(
        "/quotes",
        headers=headers,
        json={"text": "This is a valid quote text."},
    )
    assert response.status_code == 422

    # Missing text
    response = client.post(
        "/quotes",
        headers=headers,
        json={"author": "Test Author"},
    )
    assert response.status_code == 422


def test_create_quote_invalid_token(client: TestClient):
    """Test that creating a quote with an invalid token fails."""
    headers = {"Authorization": "Bearer invalid_token"}

    response = client.post(
        "/quotes",
        headers=headers,
        json={"text": "This is a test quote.", "author": "Test Author"},
    )
    assert response.status_code == 401


def test_read_all_quotes_after_creation(client: TestClient):
    """Test that created quotes appear in the list."""
    # Create a user and get a token
    client.post(
        "/users/",
        json={"username": "quoteuser_list", "email": "quote_list@example.com", "password": "password"},
    )
    login_response = client.post(
        "/token",
        data={"username": "quoteuser_list", "password": "password"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a quote
    client.post(
        "/quotes",
        headers=headers,
        json={"text": "A quote for listing test.", "author": "List Author"},
    )

    # Read all quotes and verify
    response = client.get("/quotes/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(q["text"] == "A quote for listing test." for q in data)


def test_read_all_quotes_with_pagination(client: TestClient):
    """Test reading quotes with skip and limit parameters."""
    # Create a user and get a token
    client.post(
        "/users/",
        json={"username": "quoteuser_page", "email": "quote_page@example.com", "password": "password"},
    )
    login_response = client.post(
        "/token",
        data={"username": "quoteuser_page", "password": "password"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create multiple quotes
    for i in range(5):
        client.post(
            "/quotes",
            headers=headers,
            json={"text": f"Pagination quote number {i} for testing.", "author": f"Author {i}"},
        )

    response = client.get("/quotes/all?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 2
