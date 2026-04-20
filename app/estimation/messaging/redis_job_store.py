from __future__ import annotations

import json
from datetime import datetime, timezone

from redis.asyncio import Redis

from app.shared.schemas import EstimationResponse


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class RedisJobStore:
    """Redis-backed job status store for async estimations."""

    def __init__(self, redis_url: str, key_prefix: str = "estimation:job") -> None:
        self.redis_url = redis_url
        self.key_prefix = key_prefix
        self._redis: Redis | None = None

    async def connect(self) -> None:
        self._redis = Redis.from_url(self.redis_url, decode_responses=True)
        await self._redis.ping()

    async def close(self) -> None:
        if self._redis is not None:
            await self._redis.aclose()
            self._redis = None

    def _key(self, job_id: str) -> str:
        return f"{self.key_prefix}:{job_id}"

    async def _load(self, job_id: str) -> dict | None:
        redis = self._ensure_client()
        raw = await redis.get(self._key(job_id))
        if raw is None:
            return None
        return json.loads(raw)

    async def _save(self, job_id: str, payload: dict) -> None:
        redis = self._ensure_client()
        await redis.set(self._key(job_id), json.dumps(payload))

    def _ensure_client(self) -> Redis:
        if self._redis is None:
            raise RuntimeError("RedisJobStore is not connected")
        return self._redis

    async def create_pending(self, job_id: str, correlation_id: str) -> None:
        now = _utc_now_iso()
        await self._save(
            job_id,
            {
                "job_id": job_id,
                "status": "queued",
                "progress": 0,
                "correlation_id": correlation_id,
                "created_at": now,
                "updated_at": now,
                "result": None,
                "error": None,
            },
        )

    async def set_processing(self, job_id: str) -> None:
        item = await self._load(job_id)
        if item is None:
            return
        item["status"] = "processing"
        item["progress"] = 50
        item["updated_at"] = _utc_now_iso()
        await self._save(job_id, item)

    async def set_completed(self, job_id: str, result: EstimationResponse) -> None:
        item = await self._load(job_id)
        if item is None:
            return
        item["status"] = "completed"
        item["progress"] = 100
        item["updated_at"] = _utc_now_iso()
        item["result"] = result.model_dump()
        item["error"] = None
        await self._save(job_id, item)

    async def set_failed(self, job_id: str, error: str) -> None:
        item = await self._load(job_id)
        if item is None:
            return
        item["status"] = "failed"
        item["progress"] = 100
        item["updated_at"] = _utc_now_iso()
        item["error"] = error
        await self._save(job_id, item)

    async def get(self, job_id: str) -> dict | None:
        return await self._load(job_id)
