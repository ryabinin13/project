import asyncio
from contextlib import asynccontextmanager
from aio_pika import connect, connect_robust
from fastapi import FastAPI
from app.dependencies import get_broker_consumer_service
from app.services.broker_producer import BrokerProducerService
from config import RABBIT_CONN


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.rabbit_connection = await connect_robust(RABBIT_CONN)
    app.channel = await app.rabbit_connection.channel()

    app.queue_from_user = await app.channel.declare_queue("user_to_task", durable=True)
    app.queue_to_user = await app.channel.declare_queue("user_email_from_task", durable=True)

    app.state.broker_producer_service = BrokerProducerService(app.channel)

    async def consume_user_messages():
        await app.queue_from_user.consume(get_broker_consumer_service().task_add_user)
    consumer_user_task = asyncio.create_task(consume_user_messages())

    
    yield


    consumer_user_task.cancel()
    await app.rabbit_connection.close()
