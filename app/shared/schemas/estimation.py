from typing import Literal

from pydantic import BaseModel, Field


class EstimationRequest(BaseModel):
    """Incoming request containing a meeting transcription to estimate."""

    transcription: str = Field(..., min_length=50, description="Meeting transcription text")


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
    correlation_id: str
    created_at: str
    updated_at: str
    result: EstimationResponse | None = None
    error: str | None = None
