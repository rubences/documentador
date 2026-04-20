import httpx

from app.gateway.config import get_settings
from app.shared.schemas import EstimationRequest


class EstimationServiceClientError(Exception):
    """Raised when gateway cannot retrieve a valid response from estimation service."""


def _service_headers(headers: dict[str, str] | None) -> dict[str, str]:
    return headers or {}


def _timeout_from_settings() -> httpx.Timeout:
    settings = get_settings()
    return httpx.Timeout(
        connect=settings.GATEWAY_TIMEOUT_CONNECT_SECONDS,
        read=settings.GATEWAY_TIMEOUT_READ_SECONDS,
        write=settings.GATEWAY_TIMEOUT_WRITE_SECONDS,
        pool=settings.GATEWAY_TIMEOUT_POOL_SECONDS,
    )


async def request_estimation(payload: EstimationRequest, headers: dict[str, str] | None = None) -> dict:
    """Forward an estimation request from gateway to estimation service."""
    settings = get_settings()
    url = f"{settings.ESTIMATION_SERVICE_URL}/internal/v1/estimate"

    timeout = _timeout_from_settings()
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.post(
                url,
                json=payload.model_dump(),
                headers=_service_headers(headers),
            )
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


async def request_estimation_async(
    payload: EstimationRequest,
    headers: dict[str, str] | None = None,
) -> dict:
    """Submit an async estimation job to estimation service."""
    settings = get_settings()
    url = f"{settings.ESTIMATION_SERVICE_URL}/internal/v1/estimate/async"

    timeout = _timeout_from_settings()
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.post(
                url,
                json=payload.model_dump(),
                headers=_service_headers(headers),
            )
        except httpx.HTTPError as exc:
            raise EstimationServiceClientError(f"Unable to reach estimation service: {exc}") from exc

    if response.status_code != 202:
        raise EstimationServiceClientError(
            f"Estimation service returned status {response.status_code}: {response.text}"
        )

    try:
        return response.json()
    except ValueError as exc:
        raise EstimationServiceClientError("Estimation service returned invalid JSON") from exc


async def request_estimation_status(
    job_id: str,
    headers: dict[str, str] | None = None,
) -> dict:
    """Fetch async estimation job status from estimation service."""
    settings = get_settings()
    url = f"{settings.ESTIMATION_SERVICE_URL}/internal/v1/jobs/{job_id}"

    timeout = _timeout_from_settings()
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(url, headers=_service_headers(headers))
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
