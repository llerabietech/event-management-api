import asyncio
import json
import logging

from aio_pika import ExchangeType, connect_robust

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_message(message) -> None:
    async with message.process():
        payload = json.loads(message.body)

        logger.info("Received message:")
        logger.info(payload)



async def main() -> None:
    connection = await connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()

    await channel.set_qos(prefetch_count=10)

    exchange = await channel.declare_exchange(
        "app.events",
        ExchangeType.TOPIC,
        durable=True,
    )

    queue = await channel.declare_queue(
        "event_notifications",
        durable=True,
    )

    await queue.bind(
        exchange,
        routing_key="event.created",
    )

    logger.info("Consumer started")

    async with queue.iterator() as queue_iterator:
        async for message in queue_iterator:
            await process_message(message)


if __name__ == "__main__":
    asyncio.run(main())
