import httpx

from app.gateway.config import get_settings
from app.shared.schemas import EstimationRequest


class EstimationServiceClientError(Exception):
    """Raised when gateway cannot retrieve a valid response from estimation service."""


async def request_estimation(payload: EstimationRequest) -> dict:
    """Forward an estimation request from gateway to estimation service."""
    settings = get_settings()
    url = f"{settings.ESTIMATION_SERVICE_URL}/internal/v1/estimate"

    timeout = httpx.Timeout(connect=5.0, read=120.0, write=30.0, pool=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.post(url, json=payload.model_dump())
        except httpx.HTTPError as exc:
            raise EstimationServiceClientError(f"Unable to reach estimation service: {exc}") from exc

    if response.status_code != 200:
        raise EstimationServiceClientError(
            f"Estimation service returned status {response.status_code}: {response.text}"
        )

    try:
        return response.json()
    except ValueError as exc:
        raise EstimationServiceClientError("Estimation service returned invalid JSON") from exc
