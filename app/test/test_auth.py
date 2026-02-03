from fastapi.testclient import TestClient


def test_login_for_access_token(client: TestClient):
    """Test successful login returns access token."""
    # First create a user
    client.post(
        "/users/",
        json={"username": "authuser", "email": "auth@example.com", "password": "password"},
    )

    # Correct credentials
    response = client.post(
        "/token",
        data={"username": "authuser", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_username(client: TestClient):
    """Test login with wrong username returns 401."""
    # First create a user
    client.post(
        "/users/",
        json={"username": "authuser_wrong", "email": "auth_wrong@example.com", "password": "password"},
    )

    response = client.post(
        "/token",
        data={"username": "wronguser", "password": "password"},
    )
    assert response.status_code == 401


def test_login_wrong_password(client: TestClient):
    """Test login with wrong password returns 401."""
    # First create a user
    client.post(
        "/users/",
        json={"username": "authuser_pwd", "email": "auth_pwd@example.com", "password": "password"},
    )

    response = client.post(
        "/token",
        data={"username": "authuser_pwd", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_missing_credentials(client: TestClient):
    """Test login with missing credentials returns error."""
    response = client.post(
        "/token",
        data={},
    )
    assert response.status_code == 422


def test_login_missing_password(client: TestClient):
    """Test login with missing password returns error."""
    response = client.post(
        "/token",
        data={"username": "someuser"},
    )
    assert response.status_code == 422


def test_login_missing_username(client: TestClient):
    """Test login with missing username returns error."""
    response = client.post(
        "/token",
        data={"password": "somepassword"},
    )
    assert response.status_code == 422


def test_access_protected_endpoint_with_token(client: TestClient):
    """Test that a valid token grants access to protected endpoints."""
    # Create a user
    client.post(
        "/users/",
        json={"username": "protected_user", "email": "protected@example.com", "password": "password"},
    )

    # Get token
    login_response = client.post(
        "/token",
        data={"username": "protected_user", "password": "password"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Access protected endpoint (create quote)
    response = client.post(
        "/quotes",
        headers=headers,
        json={"text": "A protected quote test.", "author": "Protected Author"},
    )
    assert response.status_code == 201


def test_access_protected_endpoint_without_token(client: TestClient):
    """Test that missing token denies access to protected endpoints."""
    response = client.post(
        "/quotes",
        json={"text": "A quote without token.", "author": "No Token Author"},
    )
    assert response.status_code == 401


def test_access_protected_endpoint_with_invalid_token(client: TestClient):
    """Test that invalid token denies access to protected endpoints."""
    headers = {"Authorization": "Bearer invalid_token_here"}
    response = client.post(
        "/quotes",
        headers=headers,
        json={"text": "A quote with invalid token.", "author": "Invalid Token Author"},
    )
    assert response.status_code == 401


def test_access_protected_endpoint_with_malformed_header(client: TestClient):
    """Test that malformed Authorization header denies access."""
    headers = {"Authorization": "NotBearer token"}
    response = client.post(
        "/quotes",
        headers=headers,
        json={"text": "A quote with malformed header.", "author": "Malformed Author"},
    )
    assert response.status_code == 401


def test_token_type_is_bearer(client: TestClient):
    """Test that the token type is 'bearer'."""
    # Create a user
    client.post(
        "/users/",
        json={"username": "bearer_user", "email": "bearer@example.com", "password": "password"},
    )

    response = client.post(
        "/token",
        data={"username": "bearer_user", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
