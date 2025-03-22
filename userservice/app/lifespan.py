import asyncio
from contextlib import asynccontextmanager
from app.dependencies import get_broker_consumer_service
from app.routers.users import user_router
from aio_pika import connect, connect_robust
from fastapi import FastAPI
from config import RABBIT_CONN
from app.services.broker_producer import BrokerProducerService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.rabbit_connection = connection = await connect_robust(RABBIT_CONN)
    app.channel = await connection.channel()

    app.queue_to_team = await app.channel.declare_queue("user_to_team", durable=True)
    app.queue_from_team = await app.channel.declare_queue("user_email_from_team", durable=True)
    app.queue_to_task = await app.channel.declare_queue("user_to_task", durable=True)
    app.queue_from_task = await app.channel.declare_queue("user_email_from_task", durable=True)

    app.state.broker_producer_service = BrokerProducerService(app.channel)
    

    async def consume_team_messages():
        await app.queue_from_team.consume(get_broker_consumer_service().check_email_from_team)

    async def consume_task_messages():
        await app.queue_from_task.consume(get_broker_consumer_service().check_email_from_task)

    consumer_team_task = asyncio.create_task(consume_team_messages())
    consumer_task_task = asyncio.create_task(consume_task_messages())


    yield

    consumer_team_task.cancel()
    consumer_task_task.cancel()
    await app.channel.close()
    await app.rabbit_connection.close()

    