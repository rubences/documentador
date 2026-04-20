from functools import lru_cache
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Estimation service settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    LLM_PROVIDER: Literal["openai", "anthropic"] = "openai"
    LLM_MODEL: str = "gpt-4o-mini"
    APP_ENV: Literal["development", "staging", "production"] = "development"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "DEBUG"
    RABBITMQ_ENABLED: bool = False
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"
    RABBITMQ_EXCHANGE: str = "estimation.jobs"
    RABBITMQ_QUEUE: str = "estimation.jobs.queue"
    RABBITMQ_ROUTING_KEY: str = "estimation.requested"
    RABBITMQ_RETRY_EXCHANGE: str = "estimation.jobs.retry"
    RABBITMQ_RETRY_QUEUE: str = "estimation.jobs.retry.queue"
    RABBITMQ_DLQ_EXCHANGE: str = "estimation.jobs.dlq"
    RABBITMQ_DLQ_QUEUE: str = "estimation.jobs.dlq.queue"
    RABBITMQ_MAX_RETRIES: int = 5
    RABBITMQ_BASE_RETRY_DELAY_MS: int = 1000
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_JOB_KEY_PREFIX: str = "estimation:job"
    OUTBOX_KEY_PREFIX: str = "estimation:outbox"
    OUTBOX_DISPATCH_BATCH_SIZE: int = 20
    OUTBOX_DISPATCH_INTERVAL_SECONDS: float = 1.0

    @model_validator(mode="after")
    def validate_api_key_for_provider(self) -> "Settings":
        """Ensure the API key for the selected LLM provider is present."""
        if self.LLM_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER is 'openai'")
        if self.LLM_PROVIDER == "anthropic" and not self.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER is 'anthropic'")
        return self


@lru_cache
def get_settings() -> Settings:
    """Return cached estimation service settings (singleton)."""
    return Settings()
