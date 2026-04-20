import secrets
import time
from functools import lru_cache
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Estimation service settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Aplicación
    APP_ENV: Literal["development", "staging", "production"] = "development"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "DEBUG"

    # Seguridad - Rate Limiting en estimation service
    RATE_LIMIT_PER_MINUTE: int = 30
    RATE_LIMIT_PER_HOUR: int = 200

    # Seguridad - CORS
    CORS_ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8080"

    # Seguridad - Autenticación interna
    # Debe coincidir con la del gateway. Se genera automáticamente si no se provee.
    INTERNAL_API_KEY: str = secrets.token_urlsafe(32)
    INTERNAL_AUTH_ENABLED: bool = True

    # LLM Provider
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    LLM_PROVIDER: Literal["openai", "anthropic"] = "openai"
    LLM_MODEL: str = "gpt-4o-mini"

    # Validación de input
    TRANSCRIPTION_MAX_LENGTH: int = 25000  # Máximo ~25k tokens

    # RabbitMQ - IMPORTANTE: cambiar credenciales en producción
    RABBITMQ_ENABLED: bool = False
    # Credenciales por defecto CAMBIAR en producción
    # Formato: amqp://username:password@host:port/vhost
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"
    # Credenciales separadas para seguridad - configurar estas en producción
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"  # ⚠️ CAMBIAR EN PRODUCCIÓN
    RABBITMQ_EXCHANGE: str = "estimation.jobs"
    RABBITMQ_QUEUE: str = "estimation.jobs.queue"
    RABBITMQ_ROUTING_KEY: str = "estimation.requested"
    RABBITMQ_RETRY_EXCHANGE: str = "estimation.jobs.retry"
    RABBITMQ_RETRY_QUEUE: str = "estimation.jobs.retry.queue"
    RABBITMQ_DLQ_EXCHANGE: str = "estimation.jobs.dlq"
    RABBITMQ_DLQ_QUEUE: str = "estimation.jobs.dlq.queue"
    RABBITMQ_MAX_RETRIES: int = 5
    RABBITMQ_BASE_RETRY_DELAY_MS: int = 1000

    # Redis - Persistencia de jobs
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_JOB_KEY_PREFIX: str = "estimation:job"
    REDIS_JOB_TTL_SECONDS: int = 86400  # 24 horas por defecto

    # Outbox
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

    @model_validator(mode="after")
    def validate_rabbitmq_credentials(self) -> "Settings":
        """Construir URL de RabbitMQ con credenciales separadas."""
        # Si RABBITMQ_USER o RABBITMQ_PASSWORD fueron configurados,
        # reconstruir la URL
        if self.RABBITMQ_USER != "guest" or self.RABBITMQ_PASSWORD != "guest":
            # Parsear URL existente y reemplazar credenciales
            import urllib.parse
            parsed = urllib.parse.urlparse(self.RABBITMQ_URL)
            self.RABBITMQ_URL = urllib.parse.urlunparse((
                parsed.scheme,
                f"{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{parsed.hostname}:{parsed.port or 5672}{parsed.path}",
                "", "", "", ""
            ))
        return self


@lru_cache
def get_settings() -> Settings:
    """Return cached estimation service settings (singleton)."""
    return Settings()
