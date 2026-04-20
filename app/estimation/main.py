import structlog
import uuid
from asyncio import CancelledError
from asyncio import Task
from asyncio import sleep
from asyncio import create_task
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
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

rabbitmq_publisher: RabbitMQPublisher | None = None
job_store: RedisJobStore | None = None
outbox_store: RedisOutboxStore | None = None
outbox_dispatcher_task: Task | None = None


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

    global rabbitmq_publisher
    global job_store
    global outbox_store
    global outbox_dispatcher_task

    job_store = RedisJobStore(
        redis_url=settings.REDIS_URL,
        key_prefix=settings.REDIS_JOB_KEY_PREFIX,
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

    log.info("estimation_service_started", environment=settings.APP_ENV)
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
attach_observability(app, service_name="estimation-service")


async def _run_estimation_job(job_id: str, transcription: str) -> None:
    log = structlog.get_logger()
    if job_store is None:
        raise RuntimeError("Redis job store is not initialized")
    await job_store.set_processing(job_id)
    try:
        result = generate_estimation(transcription)
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
async def create_estimation(request: EstimationRequest) -> EstimationResponse:
    """Generate an estimation from transcription (internal endpoint)."""
    log = structlog.get_logger()
    try:
        result = generate_estimation(request.transcription)
    except LLMServiceError as exc:
        log.error("estimation_service_error", error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return EstimationResponse(**result)


@app.post(
    "/internal/v1/estimate/async",
    response_model=AsyncEstimationAccepted,
    status_code=202,
)
async def create_estimation_async(request: EstimationRequest, http_request: Request) -> AsyncEstimationAccepted:
    """Queue an asynchronous estimation job and return tracking metadata."""
    settings = get_settings()
    correlation_id = http_request.state.correlation_id
    job_id = str(uuid.uuid4())
    event_id = str(uuid.uuid4())
    if job_store is None:
        raise HTTPException(status_code=503, detail="Redis job store is not connected")

    await job_store.create_pending(job_id=job_id, correlation_id=correlation_id)

    if settings.RABBITMQ_ENABLED:
        if outbox_store is None:
            raise HTTPException(status_code=503, detail="Outbox store is not connected")
        await outbox_store.enqueue(
            event_id=event_id,
            payload={
                "job_id": job_id,
                "transcription": request.transcription,
            },
            correlation_id=correlation_id,
        )
    else:
        create_task(_run_estimation_job(job_id=job_id, transcription=request.transcription))

    return AsyncEstimationAccepted(
        job_id=job_id,
        status="queued",
        correlation_id=correlation_id,
    )


@app.get("/internal/v1/jobs/{job_id}", response_model=AsyncEstimationStatus)
async def get_estimation_job_status(job_id: str) -> AsyncEstimationStatus:
    """Return status for an asynchronous estimation job."""
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
    return {
        "status": "healthy",
        "service": "estimation-service",
        "version": "0.2.0",
        "environment": settings.APP_ENV,
    }
