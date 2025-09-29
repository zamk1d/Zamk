import aio_pika
import asyncio
from src.services.rabbit_handlers.auth_handler import handle_auth_queue
from src.config.settings import settings


async def connect_to_rabbitmq():
    connection = await aio_pika.connect_robust(
        settings.RABBIT_URL
    )
    return connection


async def send_to_rabbitmq(queue_name: str, message: str | dict):
    connection = await connect_to_rabbitmq()
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name)

    await channel.default_exchange.publish(
        aio_pika.Message(body=message.encode()),
        routing_key=queue_name,
    )
    await connection.close()

handlers = {
    "auth_handler": handle_auth_queue
}

async def consume_messages(queue_name: str):
    connection = await connect_to_rabbitmq()
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                handler = handlers.get(queue_name)
                await handler(message.body.decode())