from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Literal


class CircuitBreakerOpenError(Exception):
    """Raised when the circuit is open and requests are rejected fast."""


@dataclass
class CircuitBreakerSnapshot:
    state: Literal["closed", "open", "half-open"]
    failure_count: int
    opened_until: float | None


class CircuitBreaker:
    """Async-safe circuit breaker with closed/open/half-open states."""

    def __init__(
        self,
        failure_threshold: int,
        recovery_timeout_seconds: float,
        half_open_success_threshold: int,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self.half_open_success_threshold = half_open_success_threshold

        self._state: Literal["closed", "open", "half-open"] = "closed"
        self._failure_count = 0
        self._half_open_success_count = 0
        self._opened_until: float | None = None
        self._lock = asyncio.Lock()

    async def before_call(self) -> None:
        async with self._lock:
            now = time.monotonic()
            if self._state == "open":
                if self._opened_until is not None and now >= self._opened_until:
                    self._state = "half-open"
                    self._half_open_success_count = 0
                else:
                    raise CircuitBreakerOpenError("Circuit breaker is open")

    async def record_success(self) -> None:
        async with self._lock:
            if self._state == "half-open":
                self._half_open_success_count += 1
                if self._half_open_success_count >= self.half_open_success_threshold:
                    self._state = "closed"
                    self._failure_count = 0
                    self._half_open_success_count = 0
                    self._opened_until = None
                return

            self._failure_count = 0
            self._opened_until = None

    async def record_failure(self) -> None:
        async with self._lock:
            if self._state == "half-open":
                self._trip_open_locked()
                return

            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                self._trip_open_locked()

    async def snapshot(self) -> CircuitBreakerSnapshot:
        async with self._lock:
            return CircuitBreakerSnapshot(
                state=self._state,
                failure_count=self._failure_count,
                opened_until=self._opened_until,
            )

    async def reset(self) -> None:
        async with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._half_open_success_count = 0
            self._opened_until = None

    async def force_open(self, duration_seconds: float) -> None:
        async with self._lock:
            self._state = "open"
            self._failure_count = 0
            self._half_open_success_count = 0
            self._opened_until = time.monotonic() + duration_seconds

    def _trip_open_locked(self) -> None:
        self._state = "open"
        self._opened_until = time.monotonic() + self.recovery_timeout_seconds
        self._failure_count = 0
        self._half_open_success_count = 0

    async def cleanup_state(self) -> None:
        """Limpia el estado del circuit breaker (para testing o memoria)."""
        async with self._lock:
            # Solo resetear contadores, mantener estado
            self._failure_count = 0
            self._half_open_success_count = 0
