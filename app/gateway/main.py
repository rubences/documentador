import structlog
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from app.gateway.clients.estimation_client import (
    EstimationServiceClientError,
    request_estimation,
    request_estimation_async,
    request_estimation_status,
)
from app.gateway.config import get_settings
from app.gateway.resilience import CircuitBreaker, CircuitBreakerOpenError
from app.shared.observability import attach_observability
from app.shared.schemas import (
    AsyncEstimationAccepted,
    AsyncEstimationStatus,
    EstimationRequest,
    EstimationResponse,
)
from app.shared.security import (
    RateLimitConfig,
    RateLimiter,
    get_rate_limiter,
    get_security_headers,
)

settings = get_settings()
circuit_breaker = CircuitBreaker(
    failure_threshold=settings.GATEWAY_CIRCUIT_BREAKER_FAILURE_THRESHOLD,
    recovery_timeout_seconds=settings.GATEWAY_CIRCUIT_BREAKER_RECOVERY_TIMEOUT_SECONDS,
    half_open_success_threshold=settings.GATEWAY_CIRCUIT_BREAKER_HALF_OPEN_SUCCESS_THRESHOLD,
)


def configure_logging() -> None:
    """Set up structlog: JSON in production, human-readable in development."""
    settings = get_settings()

    renderer = (
        structlog.processors.JSONRenderer()
        if settings.APP_ENV == "production"
        else structlog.dev.ConsoleRenderer()
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    configure_logging()
    log = structlog.get_logger()
    settings = get_settings()
    log.info("gateway_started", environment=settings.APP_ENV)
    yield
    log.info("gateway_shutdown")


app = FastAPI(
    title="Estimation API Gateway",
    description="HTTP gateway for estimation workflows",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configuración CORS segura - solo orígenes permitidos
# En desarrollo permite localhost, en producción debe configurarse
# via variable de entorno CORS_ALLOWED_ORIGINS
_security = get_settings()
_cors_origins = _security.CORS_ALLOWED_ORIGINS.split(",") if _security.CORS_ALLOWED_ORIGINS else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["authorization", "content-type", "x-request-id", "x-correlation-id", "x-internal-api-key"],
    expose_headers=["x-request-id", "x-correlation-id"],
    max_age=600,  # Cachear preflight por 10 minutos
)
attach_observability(app, service_name="api-gateway")

# Inicializar rate limiter con configuración de settings
_rate_limiter = RateLimiter(
    RateLimitConfig(
        requests_per_minute=settings.RATE_LIMIT_PER_MINUTE,
        requests_per_hour=settings.RATE_LIMIT_PER_HOUR,
    )
)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Middleware de rate limiting por IP."""
    # Excluir health y metrics del rate limiting
    if request.url.path in ["/health", "/metrics", "/docs", "/redoc"]:
        return await call_next(request)

    await _rate_limiter.check_rate_limit(request)
    response = await call_next(request)

    # Agregar headers de rate limit al response
    minute_remaining, hour_remaining = _rate_limiter.get_remaining(request)
    response.headers["X-RateLimit-Limit-Minute"] = str(settings.RATE_LIMIT_PER_MINUTE)
    response.headers["X-RateLimit-Remaining-Minute"] = str(minute_remaining)
    response.headers["X-RateLimit-Limit-Hour"] = str(settings.RATE_LIMIT_PER_HOUR)
    response.headers["X-RateLimit-Remaining-Hour"] = str(hour_remaining)
    response.headers["X-RateLimit-Reset"] = str(int(time.time() + 60))

    return response


def _downstream_headers(request: Request) -> dict[str, str]:
    return {
        "x-request-id": request.state.request_id,
        "x-correlation-id": request.state.correlation_id,
        "x-internal-api-key": settings.INTERNAL_API_KEY,
    }


@app.post("/api/v1/estimate", response_model=EstimationResponse)
async def create_estimation(request: EstimationRequest, http_request: Request) -> EstimationResponse:
    """Receive a meeting transcription and delegate the estimation generation."""
    # Rate limiting ya aplicado en middleware
    log = structlog.get_logger()
    try:
        await circuit_breaker.before_call()
    except CircuitBreakerOpenError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    try:
        result = await request_estimation(
            request,
            headers=_downstream_headers(http_request),
        )
        await circuit_breaker.record_success()
    except EstimationServiceClientError as exc:
        await circuit_breaker.record_failure()
        log.error("gateway_estimation_error", error=str(exc))
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    response = EstimationResponse(**result)
    # Agregar security headers
    for header, value in get_security_headers().items():
        # Headers se agregan en middleware de response, aquí no es posible
        # Se manejan en observability middleware
        pass

    return response


@app.post("/api/v1/estimate/async", response_model=AsyncEstimationAccepted, status_code=202)
async def create_estimation_async(
    request: EstimationRequest,
    http_request: Request,
) -> AsyncEstimationAccepted:
    """Queue an async estimation request and return job metadata."""
    log = structlog.get_logger()
    try:
        await circuit_breaker.before_call()
    except CircuitBreakerOpenError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    try:
        result = await request_estimation_async(
            request,
            headers=_downstream_headers(http_request),
        )
        await circuit_breaker.record_success()
    except EstimationServiceClientError as exc:
        await circuit_breaker.record_failure()
        log.error("gateway_estimation_async_error", error=str(exc))
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return AsyncEstimationAccepted(**result)


@app.get("/api/v1/estimate/{job_id}", response_model=AsyncEstimationStatus)
async def get_estimation_status(job_id: str, http_request: Request) -> AsyncEstimationStatus:
    """Return status for an asynchronous estimation job."""
    log = structlog.get_logger()
    try:
        await circuit_breaker.before_call()
    except CircuitBreakerOpenError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    try:
        result = await request_estimation_status(
            job_id,
            headers=_downstream_headers(http_request),
        )
        await circuit_breaker.record_success()
    except EstimationServiceClientError as exc:
        await circuit_breaker.record_failure()
        log.error("gateway_estimation_status_error", job_id=job_id, error=str(exc))
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return AsyncEstimationStatus(**result)


@app.get("/health")
async def health_check() -> dict:
    """Return gateway health status."""
    settings = get_settings()
    breaker = await circuit_breaker.snapshot()

    # Verificar conexión al estimation service
    # NOTA: Solo hacer health check a la URL configurada, NO a URLs arbitrarias
    estimation_service_healthy = True
    try:
        import httpx
        # Validar que la URL es internal/servicio conocido
        service_url = settings.ESTIMATION_SERVICE_URL
        if not service_url.startswith(("http://localhost", "http://127.0.0.1", "http://estimation-service")):
            # Solo permitir URLs internas/de contenedores
            estimation_service_healthy = False
        else:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"{service_url}/health")
                estimation_service_healthy = response.status_code == 200
    except Exception:
        estimation_service_healthy = False

    overall_status = "healthy"
    if not estimation_service_healthy:
        overall_status = "degraded"

    return {
        "status": overall_status,
        "service": "api-gateway",
        "version": "0.2.0",
        "environment": settings.APP_ENV,
        "circuit_breaker": {
            "state": breaker.state,
            "failure_count": breaker.failure_count,
            "opened_until": breaker.opened_until,
        },
        "dependencies": {
            "estimation-service": "healthy" if estimation_service_healthy else "unhealthy",
        },
    }
