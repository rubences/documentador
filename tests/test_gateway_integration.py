import asyncio
import time

from fastapi.testclient import TestClient

from app.gateway.clients.estimation_client import EstimationServiceClientError
from app.gateway.main import circuit_breaker


def _valid_payload() -> dict:
    return {
        "transcription": (
            "Cliente solicita una plataforma SaaS para gestionar suscripciones, "
            "con panel administrativo, pagos, recordatorios automáticos y API REST."
        )
    }


def test_gateway_estimate_with_mocked_latency(
    client: TestClient,
    monkeypatch,
) -> None:
    async def _slow_request_estimation(payload, headers=None):
        await asyncio.sleep(0.05)
        return {
            "estimation": "## Estimacion\n\n- Horas: 120\n- Coste: 7500 EUR",
            "model": "mock-model",
            "provider": "mock-provider",
            "usage": {
                "input_tokens": 100,
                "output_tokens": 200,
                "total_tokens": 300,
            },
        }

    monkeypatch.setattr("app.gateway.main.request_estimation", _slow_request_estimation)

    start = time.perf_counter()
    response = client.post("/api/v1/estimate", json=_valid_payload())
    elapsed = time.perf_counter() - start

    assert response.status_code == 200
    assert response.json()["provider"] == "mock-provider"
    assert elapsed >= 0.04


def test_gateway_estimate_when_downstream_fails(
    client: TestClient,
    monkeypatch,
) -> None:
    async def _failing_request_estimation(payload, headers=None):
        raise EstimationServiceClientError("simulated downstream failure")

    monkeypatch.setattr("app.gateway.main.request_estimation", _failing_request_estimation)

    response = client.post("/api/v1/estimate", json=_valid_payload())

    assert response.status_code == 502
    assert "simulated downstream failure" in response.json()["detail"]


def test_gateway_propagates_request_and_correlation_ids(
    client: TestClient,
    monkeypatch,
) -> None:
    captured_headers = {}

    async def _capture_request_estimation(payload, headers=None):
        captured_headers.update(headers or {})
        return {
            "estimation": "## Estimacion\n\n- Horas: 80\n- Coste: 5000 EUR",
            "model": "mock-model",
            "provider": "mock-provider",
            "usage": {
                "input_tokens": 90,
                "output_tokens": 130,
                "total_tokens": 220,
            },
        }

    monkeypatch.setattr("app.gateway.main.request_estimation", _capture_request_estimation)

    response = client.post(
        "/api/v1/estimate",
        json=_valid_payload(),
        headers={"x-request-id": "req-123", "x-correlation-id": "corr-999"},
    )

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "req-123"
    assert response.headers["x-correlation-id"] == "corr-999"
    assert captured_headers["x-request-id"] == "req-123"
    assert captured_headers["x-correlation-id"] == "corr-999"


def test_gateway_circuit_breaker_opens_after_repeated_failures(
    client: TestClient,
    monkeypatch,
) -> None:
    async def _failing_request_estimation(payload, headers=None):
        raise EstimationServiceClientError("simulated downstream failure")

    monkeypatch.setattr("app.gateway.main.request_estimation", _failing_request_estimation)
    asyncio.run(circuit_breaker.reset())

    for _ in range(5):
        response = client.post("/api/v1/estimate", json=_valid_payload())
        assert response.status_code == 502

    response = client.post("/api/v1/estimate", json=_valid_payload())
    assert response.status_code == 503
    assert "Circuit breaker is open" in response.json()["detail"]


def test_gateway_circuit_breaker_recovers_after_timeout(
    client: TestClient,
    monkeypatch,
) -> None:
    async def _successful_request_estimation(payload, headers=None):
        return {
            "estimation": "## Estimacion\n\n- Horas: 80\n- Coste: 5000 EUR",
            "model": "mock-model",
            "provider": "mock-provider",
            "usage": {
                "input_tokens": 90,
                "output_tokens": 130,
                "total_tokens": 220,
            },
        }

    asyncio.run(circuit_breaker.force_open(duration_seconds=0.0))
    monkeypatch.setattr("app.gateway.main.request_estimation", _successful_request_estimation)

    response = client.post("/api/v1/estimate", json=_valid_payload())
    assert response.status_code == 200
