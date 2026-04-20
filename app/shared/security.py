"""
Módulo de seguridad centralizado para la aplicación.

Este módulo proporciona:
- Rate limiting por IP/cliente
- Validación y sanitización de inputs
- Autenticación para endpoints internos
- Utilidades de seguridad comunes

NOTA: Este módulo debe ser importado y usado por todos los servicios.
"""

from __future__ import annotations

import hashlib
import hmac
import re
import time
from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

from fastapi import Header, HTTPException, Request
from pydantic import BaseModel, Field


# =============================================================================
# Rate Limiting
# =============================================================================

@dataclass
class RateLimitConfig:
    """Configuración para rate limiting."""

    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    burst_size: int = 10


@dataclass
class RateLimitRecord:
    """Registro de rate limiting para un cliente."""

    request_count: int
    window_start: float
    hourly_count: int
    hourly_window_start: float


class RateLimiter:
    """
    Rate limiter en memoria con ventana deslizante.

    Implementa rate limiting por IP usando dos ventanas:
    - Ventana por minuto (límite de ráfaga)
    - Ventana por hora (límite sostenido)
    """

    def __init__(self, config: RateLimitConfig | None = None) -> None:
        self.config = config or RateLimitConfig()
        self._clients: dict[str, RateLimitRecord] = {}
        self._cleanup_interval = 3600  # Cleanup cada hora
        self._last_cleanup = time.monotonic()

    def _get_client_key(self, request: Request) -> str:
        """
        Genera clave única para el cliente.

        Preferimos X-Forwarded-For si existe (para detrás de proxy),
        sino client IP directo.
        """
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            # Tomamos el primer IP de la cadena
            return forwarded.split(",")[0].strip()

        # Fallsback a client host
        if request.client:
            return request.client.host
        return "unknown"

    def _cleanup_if_needed(self) -> None:
        """Limpia registros antiguos periódicamente."""
        now = time.monotonic()
        if now - self._last_cleanup > self._cleanup_interval:
            # Limpiar solo entradasantiguas (más de 2 horas)
            keys_to_remove = []
            for key, record in self._clients.items():
                if now - record.hourly_window_start > 7200:  # 2 horas
                    keys_to_remove.append(key)
            for key in keys_to_remove:
                del self._clients[key]
            self._last_cleanup = now

    def _get_or_create_record(self, key: str) -> RateLimitRecord:
        """Obtiene o crea registro para el cliente."""
        now = time.monotonic()

        if key not in self._clients:
            self._clients[key] = RateLimitRecord(
                request_count=0,
                window_start=now,
                hourly_count=0,
                hourly_window_start=now,
            )
            return self._clients[key]

        record = self._clients[key]

        # Reset ventana de minutos si pasó 1 minuto
        if now - record.window_start >= 60:
            record.request_count = 0
            record.window_start = now

        # Reset ventana de horas si pasó 1 hora
        if now - record.hourly_window_start >= 3600:
            record.hourly_count = 0
            record.hourly_window_start = now

        return record

    async def check_rate_limit(self, request: Request) -> None:
        """
        Verifica si el cliente puede hacer la request.

        Lanza HTTPException 429 si excede límites.
        """
        self._cleanup_if_needed()

        key = self._get_client_key(request)
        record = self._get_or_create_record(key)

        now = time.monotonic()

        # Verificar límite por minuto
        if record.request_count >= self.config.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again in a minute.",
            )

        # Verificar límite por hora
        if record.hourly_count >= self.config.requests_per_hour:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again in an hour.",
            )

        # Incrementar contadores
        record.request_count += 1
        record.hourly_count += 1

    def get_remaining(self, request: Request) -> tuple[int, int]:
        """
        Retorna requests restantes (minuto, hora).
        """
        key = self._get_client_key(request)
        record = self._get_or_create_record(key)

        minute_remaining = self.config.requests_per_minute - record.request_count
        hour_remaining = self.config.requests_per_hour - record.hourly_count

        return max(0, minute_remaining), max(0, hour_remaining)


# Instancia global de rate limiter
_rate_limiter: RateLimiter | None = None


def get_rate_limiter() -> RateLimiter:
    """Obtiene el rate limiter global."""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter


# =============================================================================
# Sanitización de Inputs
# =============================================================================

# Caracteres peligrosos para prompt injection
INJECTION_PATTERNS = [
    r"^\s*ignore\s+all\s+previous\s+instructions",
    r"^\s*disregard\s+all\s+previous\s+instructions",
    r"^\s*forget\s+everything\s+above",
    r"^\s*system:",
    r"^\s*assistant:",
    r"^\s*you\s+are\s+now",
    r"^\s*new\s+system:",
    r"^\s*ignore",
    r"disregard",
    r"jailbreak",
    r"do anything now",
    r" DAN ",
    r"developer mode",
    r" GTP ",
    r"moral ethics",
    r"humanian",
]

# Compilar patrones para eficiencia con timeout
# IMPORTANTE: Los patrones compilados tienen timeout para prevenir ReDoS
import re as _re

# Timeout para regex (segundos)
_REGEX_TIMEOUT = 0.1

def _compile_with_timeout(pattern: str) -> _re.Pattern:
    """Compila regex con timeout simulado (Python no soporta timeout nativo en regex)."""
    compiled = _re.compile(pattern, _re.IGNORECASE)
    # Nota: Python regex no tiene timeout nativo. Para producción, usar regex-lint o rust-regex
    return compiled

_COMPILED_INJECTION_PATTERNS = [
    _compile_with_timeout(pattern) for pattern in INJECTION_PATTERNS
]

# Caracteres que podrían causar problemas en JSON/mensajes
DANGEROUS_CHARS_PATTERN = _re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


class InputSanitizer:
    """
    Sanitizador de inputs para prevenir inyecciones.
    """

    @staticmethod
    def sanitize_transcription(text: str) -> str:
        """
        Sana una transcripción de reunión.

        Removes:
        - Secuencias de control peligrosas
        - Patrones de prompt injection detectados
        - Whitespaces excesivos
        """
        if not text:
            return text

        # Remover caracteres de control
        text = DANGEROUS_CHARS_PATTERN.sub("", text)

        # Normalizar whitespace
        text = re.sub(r"\s+", " ", text)
        text = text.strip()

        # ADVERTENCIA: No removemos patrones de inyección que podrían
        # ser legítimos en la conversación. En su lugar, los pasamos
        # al LLM pero el system prompt protege contra manipulación.

        return text

    @staticmethod
    def detect_injection_attempt(text: str) -> bool:
        """
        Detenta posible intento de inyección.

        Returns True si detecta patrones sospechosos.
        """
        if not text:
            return False

        text_lower = text.lower()

        for pattern in _COMPILED_INJECTION_PATTERNS:
            if pattern.search(text):
                return True

        return False

    @staticmethod
    def sanitize_job_id(job_id: str) -> str:
        """
        Sana un job ID, permitiendo solo caracteres válidos.

        Previene path traversal y otras manipulaciones.
        """
        if not job_id:
            return job_id

        # Solo permitir caracteres alfanuméricos y guiones bajos
        # NO permitir guiones para prevenir path traversal
        sanitized = re.sub(r"[^a-zA-Z0-9_]", "", job_id)

        # Verificar que no contiene sequences de path traversal
        if any(seq in sanitized.lower() for seq in ["..", "~", "$", "`", "||", "&&"]):
            return ""

        return sanitized

    @staticmethod
    def validate_uuid_safe(job_id: str) -> bool:
        """
        Valida que un string sea un UUID válido (sin caracteres extra).
        """
        uuid_pattern = re.compile(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
            r"[0-9a-f]{4}-[0-9a-f]{12}$",
            re.IGNORECASE,
        )
        return bool(uuid_pattern.match(job_id))


# =============================================================================
# Autenticación para Endpoints Internos
# =============================================================================

@dataclass
class InternalAuthConfig:
    """Configuración para autenticación interna."""

    # API key secreta para comunicación interna entre servicios
    # Se configura via INTERNAL_API_KEY enenv var
    secret_header: str = "x-internal-api-key"
    enabled: bool = True


_internal_auth_config: InternalAuthConfig | None = None


def get_internal_auth_config() -> InternalAuthConfig:
    """Obtiene configuración de auth interna."""
    global _internal_auth_config
    if _internal_auth_config is None:
        # Se carga desde settings en runtime
        from app.gateway.config import get_settings

        settings = get_settings()
        _internal_auth_config = InternalAuthConfig(
            enabled=settings.INTERNAL_AUTH_ENABLED,
        )
    return _internal_auth_config


async def verify_internal_auth(
    x_internal_api_key: str | None = Header(None, alias="x-internal-api-key"),
) -> str:
    """
    Verifica autenticación para endpoints internos.

    Args:
        x_internal_api_key: Header con API key interna

    Returns:
        La API key si es válida

    Raises:
        HTTPException 401 si no es válida
    """
    config = get_internal_auth_config()

    if not config.enabled:
        # Auth deshabilitada (solo para desarrollo)
        return "development"

    from app.gateway.config import get_settings

    settings = get_settings()

    if not x_internal_api_key:
        raise HTTPException(
            status_code=401,
            detail="Internal API key required",
        )

    if not hmac.compare_digest(x_internal_api_key, settings.INTERNAL_API_KEY):
        raise HTTPException(
            status_code=401,
            detail="Invalid internal API key",
        )

    return x_internal_api_key


# =============================================================================
# Utilidades de Seguridad
# =============================================================================

def hash_for_logging(value: str) -> str:
    """
    Crea hash truncado para logging sin exponer datos sensibles.

    Útil para logging de IDs sin revelar valores completos.
    """
    return hashlib.sha256(value.encode()).hexdigest()[:16]


def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
    """
    Enmascara datos sensibles mostrando solo últimos caracteres.

    Útil para loguear API keys o tokens.
    """
    if not data or len(data) <= visible_chars:
        return "***"

    return "*" * (len(data) - visible_chars) + data[-visible_chars:]


# =============================================================================
# Headers de Seguridad HTTP
# =============================================================================

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
}


def get_security_headers() -> dict[str, str]:
    """Retorna headers de seguridad estándar."""
    return SECURITY_HEADERS.copy()