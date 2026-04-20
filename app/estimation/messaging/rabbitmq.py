from __future__ import annotations

import json
from collections.abc import Awaitable, Callable

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
    ) -> None:
        self.url = url
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.routing_key = routing_key
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.abc.AbstractChannel | None = None
        self._exchange: aio_pika.abc.AbstractExchange | None = None

    async def connect(self) -> None:
        self._connection = await aio_pika.connect_robust(self.url)
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=10)
        self._exchange = await self._channel.declare_exchange(
            self.exchange_name,
            ExchangeType.DIRECT,
            durable=True,
        )
        queue = await self._channel.declare_queue(self.queue_name, durable=True)
        await queue.bind(self._exchange, routing_key=self.routing_key)

    async def close(self) -> None:
        if self._connection:
            await self._connection.close()

    async def publish(self, message: dict, correlation_id: str) -> None:
        if not self._exchange:
            raise RuntimeError("RabbitMQ publisher is not connected")
        body = json.dumps(message).encode("utf-8")
        amqp_message = Message(body=body, correlation_id=correlation_id, delivery_mode=2)
        await self._exchange.publish(amqp_message, routing_key=self.routing_key)

    async def consume(self, handler: Callable[[dict, str | None], Awaitable[None]]) -> None:
        if not self._channel:
            raise RuntimeError("RabbitMQ channel is not initialized")

        queue = await self._channel.declare_queue(self.queue_name, durable=True)

        async def _on_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
            async with message.process(requeue=False):
                payload = json.loads(message.body.decode("utf-8"))
                await handler(payload, message.correlation_id)

        await queue.consume(_on_message)
