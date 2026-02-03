from fastapi.testclient import TestClient


def test_read_main(client: TestClient):
    """Test the root endpoint returns welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenido a la API de Citas Célebres"}


def test_root_endpoint_content_type(client: TestClient):
    """Test that root endpoint returns JSON with UTF-8 charset."""
    response = client.get("/")
    assert response.status_code == 200
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type
    assert "utf-8" in content_type.lower()


def test_nonexistent_endpoint(client: TestClient):
    """Test that accessing a non-existent endpoint returns 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
