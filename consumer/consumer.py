import asyncio
from functools import partial

import aio_pika

from configuration.config import load_config


async def consume():
    config = load_config("/app/.env")
    connection = await aio_pika.connect_robust(
        host=config.broker.host,
        login=config.broker.user,
        password=config.broker.password,
    )

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("test_messages", durable=True)

        await queue.consume(partial(process_message, channel=channel))
        print("Consumer started. Waiting for messages...")
        asyncio.Future()


async def process_message(message: aio_pika.IncomingMessage):
    print("че то пришло")


if __name__ == "__main__":
    asyncio.run(consume())
