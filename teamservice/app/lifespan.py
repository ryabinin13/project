import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from app.dependencies import get_consumer_service
from config import RABBIT_CONN
from app.services.consumer import ConsumerService


async def process_message(message: AbstractIncomingMessage):
    async with message.process():
        body = message.body.decode()
        print(body)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.rabbit_connection = await connect(RABBIT_CONN)
    app.channel = await app.rabbit_connection.channel()
    app.queue = await app.channel.declare_queue("user_registered", durable=True)
    async def consume_messages():
        await app.queue.consume(get_consumer_service().team_membership_create)
        try:
            await asyncio.Future()
        except KeyboardInterrupt:
            print("Exiting...")
    app.consumer_task = asyncio.create_task(consume_messages())
    yield
    app.consumer_task.cancel()
    await app.rabbit_connection.close()



