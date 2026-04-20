import time
import uuid

import structlog
from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, make_asgi_app
from starlette.responses import Response

_REQUEST_COUNTER = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["service", "method", "path", "status"],
)

_REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["service", "method", "path"],
)


def _extract_or_create_ids(request: Request) -> tuple[str, str]:
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    correlation_id = request.headers.get("x-correlation-id") or request_id
    return request_id, correlation_id


def attach_observability(app: FastAPI, service_name: str) -> None:
    """Attach middleware for request IDs, correlation IDs, and service metrics."""

    @app.middleware("http")
    async def observability_middleware(request: Request, call_next):
        request_id, correlation_id = _extract_or_create_ids(request)
        request.state.request_id = request_id
        request.state.correlation_id = correlation_id

        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            correlation_id=correlation_id,
            service=service_name,
        )

        start = time.perf_counter()
        response = Response(status_code=500)
        path = request.url.path
        try:
            response = await call_next(request)
            return response
        finally:
            duration = time.perf_counter() - start
            status_code = str(response.status_code)
            _REQUEST_COUNTER.labels(service_name, request.method, path, status_code).inc()
            _REQUEST_LATENCY.labels(service_name, request.method, path).observe(duration)

            response.headers["x-request-id"] = request_id
            response.headers["x-correlation-id"] = correlation_id
            structlog.contextvars.clear_contextvars()

    app.mount("/metrics", make_asgi_app())
