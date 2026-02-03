from fastapi.testclient import TestClient


def test_startup_check(client: TestClient):
    """Test the startup probe endpoint."""
    response = client.get("/probes/startup")
    assert response.status_code == 200
    assert response.text == "Service is started up successfully."


def test_health_check(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/probes/health")
    assert response.status_code == 200
    assert response.text == "Service is healthy."


def test_readiness_check(client: TestClient):
    """Test the readiness probe endpoint."""
    response = client.get("/probes/ready")
    assert response.status_code == 200
    assert response.text == "Service is ready to accept requests."
