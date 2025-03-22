import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from aio_pika import connect, connect_robust
from aio_pika.abc import AbstractIncomingMessage
from app.dependencies import get_broker_consumer_service
from app.services.broker_producer import BrokerProducerService
from config import RABBIT_CONN
from app.services.broker_consumer import BrokerConsumerService



@asynccontextmanager
async def lifespan(app: FastAPI):
    app.rabbit_connection = await connect_robust(RABBIT_CONN)
    app.channel = await app.rabbit_connection.channel()

    app.queue_from_user = await app.channel.declare_queue("user_to_team", durable=True)
    app.queue_to_user = await app.channel.declare_queue("user_email_from_team", durable=True)

    app.state.broker_producer_service = BrokerProducerService(app.channel, app.queue_to_user)

    async def consume_messages():
        await app.queue_from_user.consume(get_broker_consumer_service().team_membership_create)
    consumer_task = asyncio.create_task(consume_messages())

    
    yield


    consumer_task.cancel()
    await app.rabbit_connection.close()



