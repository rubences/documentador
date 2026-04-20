import structlog
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.estimation.config import get_settings
from app.estimation.services.llm_service import LLMServiceError, generate_estimation
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
    log.info("estimation_service_started", environment=settings.APP_ENV)
    yield
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
