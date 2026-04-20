from __future__ import annotations

import json
from datetime import datetime, timezone

from redis.asyncio import Redis


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class RedisOutboxStore:
    """Redis-backed outbox store to guarantee eventual RabbitMQ publication."""

    def __init__(self, redis_url: str, key_prefix: str = "estimation:outbox") -> None:
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

    def _ensure_client(self) -> Redis:
        if self._redis is None:
            raise RuntimeError("RedisOutboxStore is not connected")
        return self._redis

    def _pending_key(self) -> str:
        return f"{self.key_prefix}:pending"

    def _event_key(self, event_id: str) -> str:
        return f"{self.key_prefix}:event:{event_id}"

    async def enqueue(self, event_id: str, payload: dict, correlation_id: str) -> None:
        redis = self._ensure_client()
        now = _utc_now_iso()
        event = {
            "event_id": event_id,
            "payload": payload,
            "correlation_id": correlation_id,
            "status": "pending",
            "attempts": 0,
            "last_error": None,
            "created_at": now,
            "updated_at": now,
            "sent_at": None,
        }
        pipe = redis.pipeline(transaction=True)
        pipe.set(self._event_key(event_id), json.dumps(event))
        pipe.rpush(self._pending_key(), event_id)
        await pipe.execute()

    async def claim_pending(self, batch_size: int) -> list[dict]:
        redis = self._ensure_client()
        events: list[dict] = []

        for _ in range(batch_size):
            event_id = await redis.lpop(self._pending_key())
            if event_id is None:
                break
            raw = await redis.get(self._event_key(event_id))
            if raw is None:
                continue
            events.append(json.loads(raw))
        return events

    async def mark_sent(self, event_id: str) -> None:
        redis = self._ensure_client()
        raw = await redis.get(self._event_key(event_id))
        if raw is None:
            return
        event = json.loads(raw)
        event["status"] = "sent"
        event["updated_at"] = _utc_now_iso()
        event["sent_at"] = _utc_now_iso()
        event["last_error"] = None
        await redis.set(self._event_key(event_id), json.dumps(event))

    async def requeue(self, event_id: str, error: str) -> None:
        redis = self._ensure_client()
        raw = await redis.get(self._event_key(event_id))
        if raw is None:
            return
        event = json.loads(raw)
        event["status"] = "pending"
        event["attempts"] = int(event.get("attempts", 0)) + 1
        event["last_error"] = error
        event["updated_at"] = _utc_now_iso()

        pipe = redis.pipeline(transaction=True)
        pipe.set(self._event_key(event_id), json.dumps(event))
        pipe.rpush(self._pending_key(), event_id)
        await pipe.execute()
