import aio_pika

from configuration.config import load_config


class ProducerService:
    def __init__(self):
        config = load_config("/app/.env")
        self.host = config.broker.host
        self.user = config.broker.user
        self.password = config.broker.password

    async def send_message(self, message: str):
        connection = await aio_pika.connect_robust(host=self.host, login=self.user, password=self.password)

        async with connection:
            channel = await connection.channel()
            await channel.declare_queue("test_messages", durable=True)
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=message.encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                ),
                routing_key="test_messages",
            )
