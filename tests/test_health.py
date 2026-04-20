from fastapi.testclient import TestClient


def test_health_returns_200(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "circuit_breaker" in data
    assert data["circuit_breaker"]["state"] in {"closed", "open", "half-open"}
