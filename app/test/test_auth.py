from fastapi.testclient import TestClient

def test_login_for_access_token(client: TestClient):
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

    # Wrong username
    response = client.post(
        "/token",
        data={"username": "wronguser", "password": "password"},
    )
    assert response.status_code == 401

    # Wrong password
    response = client.post(
        "/token",
        data={"username": "authuser", "password": "wrongpassword"},
    )
    assert response.status_code == 401
