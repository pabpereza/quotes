from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data

def test_read_users(client: TestClient):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_user(client: TestClient):
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

def test_update_user(client: TestClient):
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
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"

def test_delete_user(client: TestClient):
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
