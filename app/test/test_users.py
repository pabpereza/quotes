from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    """Test creating a new user."""
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data


def test_create_user_duplicate_email(client: TestClient):
    """Test that creating a user with duplicate email fails."""
    client.post(
        "/users/",
        json={"username": "user1", "email": "duplicate@example.com", "password": "password"},
    )
    response = client.post(
        "/users/",
        json={"username": "user2", "email": "duplicate@example.com", "password": "password"},
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_create_user_missing_fields(client: TestClient):
    """Test that creating a user with missing fields fails."""
    response = client.post(
        "/users/",
        json={"username": "testuser"},
    )
    assert response.status_code == 422


def test_read_users(client: TestClient):
    """Test reading all users."""
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_read_users_with_pagination(client: TestClient):
    """Test reading users with skip and limit parameters."""
    # Create some users
    for i in range(5):
        client.post(
            "/users/",
            json={"username": f"paginationuser{i}", "email": f"pagination{i}@example.com", "password": "password"},
        )
    
    response = client.get("/users/?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 2


def test_read_user(client: TestClient):
    """Test reading a specific user by ID."""
    # First create a user to read
    response = client.post(
        "/users/",
        json={"username": "testuser2", "email": "test2@example.com", "password": "password"},
    )
    assert response.status_code == 200
    user_id = response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "testuser2"


def test_read_user_not_found(client: TestClient):
    """Test reading a non-existent user returns 404."""
    response = client.get("/users/99999")
    assert response.status_code == 404


def test_update_user(client: TestClient):
    """Test updating a user."""
    # First create a user to update
    response = client.post(
        "/users/",
        json={"username": "testuser3", "email": "test3@example.com", "password": "password"},
    )
    assert response.status_code == 200
    user_id = response.json()["id"]

    # Login to get a token
    login_response = client.post(
        "/token",
        data={"username": "testuser3", "password": "password"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(
        f"/users/{user_id}",
        headers=headers,
        json={"username": "updateduser"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"


def test_update_user_unauthenticated(client: TestClient):
    """Test that updating a user without authentication fails."""
    # First create a user to update
    response = client.post(
        "/users/",
        json={"username": "testuser_unauth", "email": "unauth@example.com", "password": "password"},
    )
    user_id = response.json()["id"]

    response = client.put(
        f"/users/{user_id}",
        json={"username": "updateduser"},
    )
    assert response.status_code == 401


def test_update_user_not_found(client: TestClient):
    """Test that updating a non-existent user returns 404."""
    # Create a user and get token
    client.post(
        "/users/",
        json={"username": "updateuser_nf", "email": "update_nf@example.com", "password": "password"},
    )
    login_response = client.post(
        "/token",
        data={"username": "updateuser_nf", "password": "password"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put(
        "/users/99999",
        headers=headers,
        json={"username": "updateduser"},
    )
    assert response.status_code == 404


def test_delete_user(client: TestClient):
    """Test deleting a user."""
    # First create a user to delete
    response = client.post(
        "/users/",
        json={"username": "testuser4", "email": "test4@example.com", "password": "password"},
    )
    assert response.status_code == 200
    user_id = response.json()["id"]

    # Login to get a token
    login_response = client.post(
        "/token",
        data={"username": "testuser4", "password": "password"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/users/{user_id}", headers=headers)
    assert response.status_code == 200

    # Verify user is deleted
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


def test_delete_user_unauthenticated(client: TestClient):
    """Test that deleting a user without authentication fails."""
    # First create a user to delete
    response = client.post(
        "/users/",
        json={"username": "delete_unauth", "email": "delete_unauth@example.com", "password": "password"},
    )
    user_id = response.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 401


def test_delete_user_not_found(client: TestClient):
    """Test that deleting a non-existent user returns 404."""
    # Create a user and get token
    client.post(
        "/users/",
        json={"username": "deleteuser_nf", "email": "delete_nf@example.com", "password": "password"},
    )
    login_response = client.post(
        "/token",
        data={"username": "deleteuser_nf", "password": "password"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete("/users/99999", headers=headers)
    assert response.status_code == 404

