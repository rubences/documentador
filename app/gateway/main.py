import structlog
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.gateway.clients.estimation_client import (
    EstimationServiceClientError,
    request_estimation,
)
from app.gateway.config import get_settings
from app.shared.schemas import EstimationRequest, EstimationResponse


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/estimate", response_model=EstimationResponse)
async def create_estimation(request: EstimationRequest) -> EstimationResponse:
    """Receive a meeting transcription and delegate the estimation generation."""
    log = structlog.get_logger()
    try:
        result = await request_estimation(request)
    except EstimationServiceClientError as exc:
        log.error("gateway_estimation_error", error=str(exc))
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return EstimationResponse(**result)


@app.get("/health")
async def health_check() -> dict:
    """Return gateway health status."""
    settings = get_settings()
    return {
        "status": "healthy",
        "service": "api-gateway",
        "version": "0.2.0",
        "environment": settings.APP_ENV,
    }
