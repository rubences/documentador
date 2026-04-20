from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.estimation.config import get_settings


class EstimationRequest(BaseModel):
    """Incoming request containing a meeting transcription to estimate."""

    transcription: str = Field(
        ...,
        min_length=50,
        max_length=25000,  # ~25k tokens máximo
        description="Meeting transcription text (50-25000 chars)",
    )

    @field_validator("transcription", mode="before")
    @classmethod
    def validate_transcription_length(cls, v: str) -> str:
        """Valida que la transcripción no exceda el máximo configurado."""
        if not v:
            return v

        # Obtener configuración
        try:
            settings = get_settings()
            max_length = settings.TRANSCRIPTION_MAX_LENGTH
        except Exception:
            max_length = 25000

        if len(v) > max_length:
            raise ValueError(
                f"Transcription exceeds maximum length of {max_length} characters"
            )

        return v


class TokenUsage(BaseModel):
    """Token consumption details from the LLM call."""

    input_tokens: int
    output_tokens: int
    total_tokens: int


class EstimationResponse(BaseModel):
    """Response containing the generated estimation and metadata."""

    estimation: str = Field(..., description="Generated software estimation in markdown")
    model: str = Field(..., description="LLM model used")
    provider: str = Field(..., description="LLM provider used")
    usage: TokenUsage


class AsyncEstimationAccepted(BaseModel):
    """Acknowledgement returned when async estimation is accepted."""

    job_id: str = Field(..., description="Asynchronous estimation job identifier")
    status: Literal["queued"] = "queued"
    correlation_id: str = Field(..., description="Distributed correlation identifier")


class AsyncEstimationStatus(BaseModel):
    """Status payload for asynchronous estimation jobs."""

    job_id: str
    status: Literal["queued", "processing", "completed", "failed"]
    progress: int = Field(..., ge=0, le=100)
    correlation_id: str
    created_at: str
    updated_at: str
    result: EstimationResponse | None = None
    error: str | None = None
