from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from typing import Any

import aio_pika
from aio_pika import ExchangeType, Message


class RabbitMQPublisher:
    """RabbitMQ publisher and consumer bootstrap for estimation jobs."""

    def __init__(
        self,
        url: str,
        exchange_name: str,
        queue_name: str,
        routing_key: str,
        retry_exchange_name: str,
        retry_queue_name: str,
        dlq_exchange_name: str,
        dlq_queue_name: str,
        max_retries: int,
        base_retry_delay_ms: int,
    ) -> None:
        self.url = url
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.retry_exchange_name = retry_exchange_name
        self.retry_queue_name = retry_queue_name
        self.dlq_exchange_name = dlq_exchange_name
        self.dlq_queue_name = dlq_queue_name
        self.max_retries = max_retries
        self.base_retry_delay_ms = base_retry_delay_ms
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.abc.AbstractChannel | None = None
        self._exchange: aio_pika.abc.AbstractExchange | None = None
        self._retry_exchange: aio_pika.abc.AbstractExchange | None = None
        self._dlq_exchange: aio_pika.abc.AbstractExchange | None = None

    async def connect(self) -> None:
        self._connection = await aio_pika.connect_robust(self.url)
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=10)
        self._exchange = await self._channel.declare_exchange(
            self.exchange_name,
            ExchangeType.DIRECT,
            durable=True,
        )
        self._retry_exchange = await self._channel.declare_exchange(
            self.retry_exchange_name,
            ExchangeType.DIRECT,
            durable=True,
        )
        self._dlq_exchange = await self._channel.declare_exchange(
            self.dlq_exchange_name,
            ExchangeType.DIRECT,
            durable=True,
        )

        main_queue = await self._channel.declare_queue(self.queue_name, durable=True)
        await main_queue.bind(self._exchange, routing_key=self.routing_key)

        retry_queue = await self._channel.declare_queue(
            self.retry_queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": self.exchange_name,
                "x-dead-letter-routing-key": self.routing_key,
            },
        )
        await retry_queue.bind(self._retry_exchange, routing_key=self.routing_key)

        dlq_queue = await self._channel.declare_queue(self.dlq_queue_name, durable=True)
        await dlq_queue.bind(self._dlq_exchange, routing_key=self.routing_key)

    async def close(self) -> None:
        if self._connection:
            await self._connection.close()

    async def publish(
        self,
        message: dict,
        correlation_id: str,
        headers: dict[str, Any] | None = None,
        expiration_ms: int | None = None,
    ) -> None:
        if not self._exchange:
            raise RuntimeError("RabbitMQ publisher is not connected")
        body = json.dumps(message).encode("utf-8")
        amqp_message = Message(
            body=body,
            correlation_id=correlation_id,
            delivery_mode=2,
            headers=headers or {},
            expiration=str(expiration_ms) if expiration_ms is not None else None,
        )
        await self._exchange.publish(amqp_message, routing_key=self.routing_key)

    async def consume(self, handler: Callable[[dict, str | None], Awaitable[None]]) -> None:
        if not self._channel:
            raise RuntimeError("RabbitMQ channel is not initialized")

        queue = await self._channel.declare_queue(self.queue_name, durable=True)

        async def _on_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
            async with message.process(requeue=False, ignore_processed=True):
                payload = json.loads(message.body.decode("utf-8"))
                try:
                    await handler(payload, message.correlation_id)
                except Exception as exc:
                    await self._handle_failed_message(message=message, payload=payload, error=exc)

        await queue.consume(_on_message)

    async def _handle_failed_message(
        self,
        message: aio_pika.abc.AbstractIncomingMessage,
        payload: dict,
        error: Exception,
    ) -> None:
        retry_count = int((message.headers or {}).get("x-retry-count", 0))

        if retry_count >= self.max_retries:
            await self._publish_to_dlq(payload=payload, correlation_id=message.correlation_id, error=error)
            return

        next_retry = retry_count + 1
        delay_ms = self.base_retry_delay_ms * (2 ** retry_count)
        await self._publish_to_retry(
            payload=payload,
            correlation_id=message.correlation_id,
            retry_count=next_retry,
            delay_ms=delay_ms,
        )

    async def _publish_to_retry(
        self,
        payload: dict,
        correlation_id: str | None,
        retry_count: int,
        delay_ms: int,
    ) -> None:
        if not self._retry_exchange:
            raise RuntimeError("Retry exchange is not initialized")
        body = json.dumps(payload).encode("utf-8")
        retry_message = Message(
            body=body,
            correlation_id=correlation_id,
            delivery_mode=2,
            headers={"x-retry-count": retry_count},
            expiration=str(delay_ms),
        )
        await self._retry_exchange.publish(retry_message, routing_key=self.routing_key)

    async def _publish_to_dlq(
        self,
        payload: dict,
        correlation_id: str | None,
        error: Exception,
    ) -> None:
        if not self._dlq_exchange:
            raise RuntimeError("DLQ exchange is not initialized")
        body = json.dumps(payload).encode("utf-8")
        dlq_message = Message(
            body=body,
            correlation_id=correlation_id,
            delivery_mode=2,
            headers={"error": str(error), "final": True},
        )
        await self._dlq_exchange.publish(dlq_message, routing_key=self.routing_key)
