import structlog
import uuid
from asyncio import CancelledError
from asyncio import Task
from asyncio import sleep
from asyncio import create_task
from contextlib import asynccontextmanager
from typing import Annotated

import hmac
from fastapi import Depends, FastAPI, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware

from app.estimation.config import get_settings
from app.estimation.messaging import RabbitMQPublisher, RedisJobStore, RedisOutboxStore
from app.estimation.services.llm_service import LLMServiceError, generate_estimation
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
    InputSanitizer,
)

rabbitmq_publisher: RabbitMQPublisher | None = None
job_store: RedisJobStore | None = None
outbox_store: RedisOutboxStore | None = None
outbox_dispatcher_task: Task | None = None
_rate_limiter: RateLimiter | None = None


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


async def verify_internal_auth(
    x_internal_api_key: Annotated[str | None, Header(alias="x-internal-api-key")] = None,
) -> str:
    """
    Verifica autenticación para endpoints internos.

    Returns:
        API key si es válida

    Raises:
        HTTPException 401 si no es válida
    """
    settings = get_settings()

    if not settings.INTERNAL_AUTH_ENABLED:
        # Auth deshabilitada (solo para desarrollo local)
        return "development-disabled"

    if not x_internal_api_key:
        raise HTTPException(
            status_code=401,
            detail="Internal API key required. Header 'x-internal-api-key' is missing.",
        )

    if not hmac.compare_digest(x_internal_api_key, settings.INTERNAL_API_KEY):
        raise HTTPException(
            status_code=401,
            detail="Invalid internal API key",
        )

    return x_internal_api_key


# Alias para usar en Depends
InternalAuth = Annotated[str, Depends(verify_internal_auth)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    configure_logging()
    log = structlog.get_logger()
    settings = get_settings()

    global rabbitmq_publisher
    global job_store
    global outbox_store
    global outbox_dispatcher_task
    global _rate_limiter

    # Inicializar rate limiter
    _rate_limiter = RateLimiter(
        RateLimitConfig(
            requests_per_minute=settings.RATE_LIMIT_PER_MINUTE,
            requests_per_hour=settings.RATE_LIMIT_PER_HOUR,
        )
    )

    job_store = RedisJobStore(
        redis_url=settings.REDIS_URL,
        key_prefix=settings.REDIS_JOB_KEY_PREFIX,
        ttl_seconds=settings.REDIS_JOB_TTL_SECONDS,
    )
    await job_store.connect()

    outbox_store = RedisOutboxStore(
        redis_url=settings.REDIS_URL,
        key_prefix=settings.OUTBOX_KEY_PREFIX,
    )
    await outbox_store.connect()

    if settings.RABBITMQ_ENABLED:
        rabbitmq_publisher = RabbitMQPublisher(
            url=settings.RABBITMQ_URL,
            exchange_name=settings.RABBITMQ_EXCHANGE,
            queue_name=settings.RABBITMQ_QUEUE,
            routing_key=settings.RABBITMQ_ROUTING_KEY,
            retry_exchange_name=settings.RABBITMQ_RETRY_EXCHANGE,
            retry_queue_name=settings.RABBITMQ_RETRY_QUEUE,
            dlq_exchange_name=settings.RABBITMQ_DLQ_EXCHANGE,
            dlq_queue_name=settings.RABBITMQ_DLQ_QUEUE,
            max_retries=settings.RABBITMQ_MAX_RETRIES,
            base_retry_delay_ms=settings.RABBITMQ_BASE_RETRY_DELAY_MS,
        )
        await rabbitmq_publisher.connect()
        await rabbitmq_publisher.consume(_process_queue_message)
        log.info("rabbitmq_consumer_started", queue=settings.RABBITMQ_QUEUE)
        outbox_dispatcher_task = create_task(_outbox_dispatch_loop())
        log.info("outbox_dispatcher_started")

    log.info(
        "estimation_service_started",
        environment=settings.APP_ENV,
        internal_auth_enabled=settings.INTERNAL_AUTH_ENABLED,
    )
    yield
    if outbox_dispatcher_task:
        outbox_dispatcher_task.cancel()
        try:
            await outbox_dispatcher_task
        except CancelledError:
            pass
    if rabbitmq_publisher:
        await rabbitmq_publisher.close()
    if outbox_store:
        await outbox_store.close()
    if job_store:
        await job_store.close()
    log.info("estimation_service_shutdown")


app = FastAPI(
    title="Estimation Service",
    description="Internal estimation generation microservice",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS seguro - origins desde configuración
# En producción, configurar CORS_ALLOWED_ORIGINS en variables de entorno
_security = get_settings()
# Por defecto permitir localhost, pero leer de configuración
_cors_origins_env = getattr(_security, 'CORS_ALLOWED_ORIGINS', None)
if _cors_origins_env:
    _cors_origins = [o.strip() for o in _cors_origins_env.split(",") if o.strip()]
else:
    _cors_origins = ["http://localhost:3000", "http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["content-type", "x-request-id", "x-correlation-id", "x-internal-api-key"],
    expose_headers=["x-request-id", "x-correlation-id"],
    max_age=600,
)
attach_observability(app, service_name="estimation-service")


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Middleware de rate limiting por IP."""
    if request.url.path in ["/health", "/metrics", "/docs", "/redoc"]:
        return await call_next(request)

    # Solo rate limitear endpoints internos
    if request.url.path.startswith("/internal/"):
        await _rate_limiter.check_rate_limit(request)

    response = await call_next(request)
    return response


async def _run_estimation_job(job_id: str, transcription: str) -> None:
    log = structlog.get_logger()
    if job_store is None:
        raise RuntimeError("Redis job store is not initialized")

    # Sanitizar transcripción antes de procesar
    sanitized_transcription = InputSanitizer.sanitize_transcription(transcription)

    await job_store.set_processing(job_id)
    try:
        result = generate_estimation(sanitized_transcription)
        await job_store.set_completed(job_id, EstimationResponse(**result))
    except LLMServiceError as exc:
        log.error("estimation_async_job_failed", job_id=job_id, error=str(exc))
        await job_store.set_failed(job_id, str(exc))


async def _outbox_dispatch_loop() -> None:
    log = structlog.get_logger()
    settings = get_settings()
    if outbox_store is None or rabbitmq_publisher is None:
        raise RuntimeError("Outbox dispatcher requires initialized stores and publisher")

    while True:
        events = await outbox_store.claim_pending(settings.OUTBOX_DISPATCH_BATCH_SIZE)
        if not events:
            await sleep(settings.OUTBOX_DISPATCH_INTERVAL_SECONDS)
            continue

        for event in events:
            event_id = event["event_id"]
            try:
                await rabbitmq_publisher.publish(
                    message=event["payload"],
                    correlation_id=event["correlation_id"],
                    headers={"x-outbox-event-id": event_id},
                )
                await outbox_store.mark_sent(event_id)
            except Exception as exc:
                log.error("outbox_dispatch_failed", event_id=event_id, error=str(exc))
                await outbox_store.requeue(event_id, str(exc))


async def _process_queue_message(payload: dict, correlation_id: str | None) -> None:
    log = structlog.get_logger()
    job_id = payload.get("job_id")
    transcription = payload.get("transcription")
    if not job_id or not transcription:
        log.error("invalid_estimation_job_message", payload=payload, correlation_id=correlation_id)
        return
    await _run_estimation_job(job_id=job_id, transcription=transcription)


@app.post("/internal/v1/estimate", response_model=EstimationResponse)
async def create_estimation(
    request: EstimationRequest,
    _auth: InternalAuth,
) -> EstimationResponse:
    """
    Generate an estimation from transcription (internal endpoint).

    Requires x-internal-api-key header for authentication.
    """
    log = structlog.get_logger()

    # Sanitizar input
    sanitized_transcription = InputSanitizer.sanitize_transcription(request.transcription)

    try:
        result = generate_estimation(sanitized_transcription)
    except LLMServiceError as exc:
        log.error("estimation_service_error", error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return EstimationResponse(**result)


@app.post(
    "/internal/v1/estimate/async",
    response_model=AsyncEstimationAccepted,
    status_code=202,
)
async def create_estimation_async(
    request: EstimationRequest,
    http_request: Request,
    _auth: InternalAuth,
) -> AsyncEstimationAccepted:
    """
    Queue an asynchronous estimation job and return tracking metadata.

    Requires x-internal-api-key header for authentication.
    """
    settings = get_settings()
    correlation_id = http_request.state.correlation_id
    job_id = str(uuid.uuid4())
    event_id = str(uuid.uuid4())

    if job_store is None:
        raise HTTPException(status_code=503, detail="Redis job store is not connected")

    # Sanitizar transcripción
    sanitized_transcription = InputSanitizer.sanitize_transcription(request.transcription)

    await job_store.create_pending(job_id=job_id, correlation_id=correlation_id)

    if settings.RABBITMQ_ENABLED:
        if outbox_store is None:
            raise HTTPException(status_code=503, detail="Outbox store is not connected")
        await outbox_store.enqueue(
            event_id=event_id,
            payload={
                "job_id": job_id,
                "transcription": sanitized_transcription,
            },
            correlation_id=correlation_id,
        )
    else:
        create_task(_run_estimation_job(job_id=job_id, transcription=sanitized_transcription))

    return AsyncEstimationAccepted(
        job_id=job_id,
        status="queued",
        correlation_id=correlation_id,
    )


@app.get("/internal/v1/jobs/{job_id}", response_model=AsyncEstimationStatus)
async def get_estimation_job_status(
    job_id: str,
    _auth: InternalAuth,
) -> AsyncEstimationStatus:
    """
    Return status for an asynchronous estimation job.

    Requires x-internal-api-key header for authentication.
    """
    # Validar job_id como UUID
    if not InputSanitizer.validate_uuid_safe(job_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid job_id format. Must be a valid UUID.",
        )

    if job_store is None:
        raise HTTPException(status_code=503, detail="Redis job store is not connected")

    item = await job_store.get(job_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Job not found: {job_id}")

    return AsyncEstimationStatus(**item)


@app.get("/health")
async def health_check() -> dict:
    """Return estimation-service health status."""
    settings = get_settings()

    # Verificar conexión a Redis
    redis_healthy = False
    if job_store:
        try:
            redis_healthy = await job_store.ping()
        except Exception:
            redis_healthy = False

    return {
        "status": "healthy" if redis_healthy else "degraded",
        "service": "estimation-service",
        "version": "0.2.0",
        "environment": settings.APP_ENV,
        "dependencies": {
            "redis": "healthy" if redis_healthy else "unhealthy",
            "rabbitmq": "disabled" if not settings.RABBITMQ_ENABLED else "unknown",
        },
    }
