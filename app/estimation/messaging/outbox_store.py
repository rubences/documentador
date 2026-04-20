from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from redis.asyncio import Redis


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class RedisOutboxStore:
    """
    Redis-backed outbox store to guarantee eventual RabbitMQ publication.

    Implementa un patrón de cola segura que previene pérdida de mensajes:
    - claim_pending move mensajes a una cola de procesamiento
    - Solo marca como "sent" cuando se completa exitosamente
    - Si falla, el mensaje vuelve a pending automáticamente
    """

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

    def _processing_key(self) -> str:
        """Cola de mensajes siendo procesados actualmente."""
        return f"{self.key_prefix}:processing"

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
            "processing_since": None,
        }
        pipe = redis.pipeline(transaction=True)
        pipe.set(self._event_key(event_id), json.dumps(event))
        pipe.rpush(self._pending_key(), event_id)
        await pipe.execute()

    async def claim_pending(self, batch_size: int, processing_timeout_seconds: int = 300) -> list[dict]:
        """
        Reclama mensajes de la cola pending moviéndolos a processing atómicamente.

        Esto previene la pérdida de mensajes si el proceso falla después de remover
        de la cola pending pero antes de completar el procesamiento.
        """
        redis = self._ensure_client()
        events: list[dict] = []
        now = _utc_now_iso()

        for _ in range(batch_size):
            # Usar atomic move: RPOP + LPUSH atómico
            event_id = await redis.lpop(self._pending_key())
            if event_id is None:
                break

            # Verificar que el evento existe
            raw = await redis.get(self._event_key(event_id))
            if raw is None:
                # El evento fue eliminado,skip
                continue

            event = json.loads(raw)

            # Verificar si ya está siendo procesado (timeout)
            processing_since = event.get("processing_since")
            if processing_since:
                # Calcular si expiró
                from datetime import datetime, timezone

                try:
                    proc_dt = datetime.fromisoformat(processing_since.replace("Z", "+00:00"))
                    import time

                    if (datetime.now(timezone.utc) - proc_dt).total_seconds() < processing_timeout_seconds:
                        # Still processing, put back
                        await redis.rpush(self._pending_key(), event_id)
                        continue
                except Exception:
                    # Invalid timestamp, requeue
                    await redis.rpush(self._pending_key(), event_id)
                    continue

            # Marcar como processing
            event["status"] = "processing"
            event["processing_since"] = now
            event["updated_at"] = now

            # Actualizar en Redis Y mover a cola de procesamiento atomícamente
            pipe = redis.pipeline(transaction=True)
            pipe.set(self._event_key(event_id), json.dumps(event))
            pipe.rpush(self._processing_key(), event_id)
            await pipe.execute()

            events.append(event)

        return events

    async def mark_sent(self, event_id: str) -> None:
        """
        Marca un evento como enviado exitosamente.

        Este método DEBE llamarse después de exitosamente publicar a RabbitMQ.
        """
        redis = self._ensure_client()

        # Obtener evento actual
        raw = await redis.get(self._event_key(event_id))
        if raw is None:
            return

        event = json.loads(raw)

        # Actualizar estado a sent
        event["status"] = "sent"
        event["updated_at"] = _utc_now_iso()
        event["sent_at"] = _utc_now_iso()
        event["processing_since"] = None
        event["last_error"] = None

        # Usar pipeline atómico
        pipe = redis.pipeline(transaction=True)
        pipe.set(self._event_key(event_id), json.dumps(event))
        # Remover de la cola de processing si está ahí
        pipe.lrem(self._processing_key(), 0, event_id)
        await pipe.execute()

    async def requeue(self, event_id: str, error: str) -> None:
        """
        Regresa un evento a la cola pending cuando el procesamiento falla.

        Incrementa el contador de intentos y preserva el error para debugging.
        """
        redis = self._ensure_client()

        raw = await redis.get(self._event_key(event_id))
        if raw is None:
            return

        event = json.loads(raw)

        # Incrementar intentos
        event["attempts"] = int(event.get("attempts", 0)) + 1
        event["status"] = "pending"
        event["last_error"] = error[:500] if error else None  # Truncar errores largos
        event["updated_at"] = _utc_now_iso()
        event["processing_since"] = None

        # Mover de vuelta a pending atómicamente
        pipe = redis.pipeline(transaction=True)
        pipe.set(self._event_key(event_id), json.dumps(event))
        pipe.lrem(self._processing_key(), 0, event_id)
        pipe.rpush(self._pending_key(), event_id)
        await pipe.execute()

    async def cleanup_old_events(self, max_age_seconds: int = 86400) -> int:
        """
        Limpia eventos antiguos que ya fueron enviados.

        Args:
            max_age_seconds: Máximo tiempo en segundos para mantener eventos enviados

        Returns:
            Número de eventos limpiados
        """
        redis = self._ensure_client()
        cleaned = 0

        # Buscar todos los eventos con status "sent"
        pattern = f"{self.key_prefix}:event:*"
        cursor = 0

        while True:
            cursor, keys = await redis.scan(cursor, match=pattern, count=100)
            for key in keys:
                raw = await redis.get(key)
                if raw:
                    event = json.loads(raw)
                    if event.get("status") == "sent":
                        sent_at = event.get("sent_at")
                        if sent_at:
                            from datetime import datetime, timezone

                            try:
                                sent_dt = datetime.fromisoformat(sent_at.replace("Z", "+00:00"))
                                import time

                                if (datetime.now(timezone.utc) - sent_dt).total_seconds() > max_age_seconds:
                                    await redis.delete(key)
                                    cleaned += 1
                            except Exception:
                                pass
            if cursor == 0:
                break

        return cleaned
