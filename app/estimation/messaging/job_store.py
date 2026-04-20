from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from app.shared.schemas import EstimationResponse


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class EstimationJobStore:
    """In-memory job status store for async estimations."""

    def __init__(self) -> None:
        self._data: dict[str, dict] = {}
        self._lock = asyncio.Lock()

    async def create_pending(self, job_id: str, correlation_id: str) -> None:
        async with self._lock:
            self._data[job_id] = {
                "job_id": job_id,
                "status": "queued",
                "correlation_id": correlation_id,
                "created_at": _utc_now_iso(),
                "updated_at": _utc_now_iso(),
                "result": None,
                "error": None,
            }

    async def set_processing(self, job_id: str) -> None:
        async with self._lock:
            if job_id in self._data:
                self._data[job_id]["status"] = "processing"
                self._data[job_id]["updated_at"] = _utc_now_iso()

    async def set_completed(self, job_id: str, result: EstimationResponse) -> None:
        async with self._lock:
            if job_id in self._data:
                self._data[job_id]["status"] = "completed"
                self._data[job_id]["updated_at"] = _utc_now_iso()
                self._data[job_id]["result"] = result.model_dump()
                self._data[job_id]["error"] = None

    async def set_failed(self, job_id: str, error: str) -> None:
        async with self._lock:
            if job_id in self._data:
                self._data[job_id]["status"] = "failed"
                self._data[job_id]["updated_at"] = _utc_now_iso()
                self._data[job_id]["error"] = error

    async def get(self, job_id: str) -> dict | None:
        async with self._lock:
            item = self._data.get(job_id)
            return dict(item) if item else None


job_store = EstimationJobStore()
