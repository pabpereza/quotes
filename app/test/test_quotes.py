from fastapi.testclient import TestClient

def test_read_quotes(client: TestClient):
    response = client.get("/quotes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_quote(client: TestClient):
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

def test_create_quote_unauthenticated(client: TestClient):
    response = client.post(
        "/quotes",
        json={"text": "This is a test quote.", "author": "Test Author"},
    )
    assert response.status_code == 401
