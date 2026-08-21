import json
from typing import Any

import aio_pika
from aio_pika import DeliveryMode, ExchangeType, Message, connect_robust


class RabbitClient:
    def __init__(
        self,
        url: str,
        exchange_name: str = "app.events",
    ):
        self.url = url
        self.exchange_name = exchange_name

        self.connection: aio_pika.abc.AbstractRobustConnection | None = None
        self.channel: aio_pika.abc.AbstractChannel | None = None
        self.exchange: aio_pika.abc.AbstractExchange | None = None

    async def connect(self) -> None:
        self.connection = await connect_robust(self.url)

        self.channel = await self.connection.channel()

        self.exchange = await self.channel.declare_exchange(
            self.exchange_name,
            ExchangeType.TOPIC,
            durable=True,
        )

    async def close(self) -> None:
        if self.connection is not None:
            await self.connection.close()

    async def publish(
        self,
        routing_key: str,
        payload: dict[str, Any],
    ) -> None:
        if self.exchange is None:
            raise RuntimeError("RabbitMQ is not connected")

        message = Message(
            body=json.dumps(payload).encode(),
            content_type="application/json",
            delivery_mode=DeliveryMode.PERSISTENT,
        )

        await self.exchange.publish(
            message,
            routing_key=routing_key,
        )
