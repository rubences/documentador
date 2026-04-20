from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Gateway settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_ENV: Literal["development", "staging", "production"] = "development"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "DEBUG"
    ESTIMATION_SERVICE_URL: str = "http://estimation-service:8001"
    GATEWAY_TIMEOUT_CONNECT_SECONDS: float = 2.0
    GATEWAY_TIMEOUT_READ_SECONDS: float = 10.0
    GATEWAY_TIMEOUT_WRITE_SECONDS: float = 5.0
    GATEWAY_TIMEOUT_POOL_SECONDS: float = 2.0
    GATEWAY_CIRCUIT_BREAKER_FAILURE_THRESHOLD: int = 5
    GATEWAY_CIRCUIT_BREAKER_RECOVERY_TIMEOUT_SECONDS: float = 30.0
    GATEWAY_CIRCUIT_BREAKER_HALF_OPEN_SUCCESS_THRESHOLD: int = 2


@lru_cache
def get_settings() -> Settings:
    """Return cached gateway settings (singleton)."""
    return Settings()
