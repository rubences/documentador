import secrets
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Gateway settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Aplicación
    APP_ENV: Literal["development", "staging", "production"] = "development"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "DEBUG"

    # Seguridad - CORS
    # Lista de orígenes separados por coma. Solo estos orígenes pueden acceder.
    # En desarrollo: "http://localhost:3000,http://localhost:8080"
    # En producción: configurar origenes específicos de la aplicación frontend
    CORS_ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8080"

    # Seguridad - Rate Limiting
    # Límites por IP del cliente
    RATE_LIMIT_PER_MINUTE: int = 30  # Ráfaga máxima
    RATE_LIMIT_PER_HOUR: int = 200   # Límite sostenido

    # Seguridad - Autenticación interna
    # API key para comunicación entre servicios (gateway <-> estimation-service)
    # IMPORTANTE: cambiar en producción con valor aleatorio
    INTERNAL_API_KEY: str = secrets.token_urlsafe(32)
    INTERNAL_AUTH_ENABLED: bool = True

    # Microservicios
    ESTIMATION_SERVICE_URL: str = "http://estimation-service:8001"

    # Timeouts
    GATEWAY_TIMEOUT_CONNECT_SECONDS: float = 2.0
    GATEWAY_TIMEOUT_READ_SECONDS: float = 10.0
    GATEWAY_TIMEOUT_WRITE_SECONDS: float = 5.0
    GATEWAY_TIMEOUT_POOL_SECONDS: float = 2.0

    # Circuit Breaker
    GATEWAY_CIRCUIT_BREAKER_FAILURE_THRESHOLD: int = 5
    GATEWAY_CIRCUIT_BREAKER_RECOVERY_TIMEOUT_SECONDS: float = 30.0
    GATEWAY_CIRCUIT_BREAKER_HALF_OPEN_SUCCESS_THRESHOLD: int = 2


@lru_cache
def get_settings() -> Settings:
    """Return cached gateway settings (singleton)."""
    return Settings()
