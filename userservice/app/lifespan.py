import asyncio
from contextlib import asynccontextmanager
import os
from aio_pika import connect_robust
import aio_pika
from fastapi import FastAPI
from alembic import command
from alembic.config import Config
from app.database import Base, async_engine
from app.dependencies import get_broker_consumer_service
from app.services.broker_producer import BrokerProducerService
from config import RABBIT_CONN
from app.const import RABBIT_ATTEMPTS
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 

console_handler = logging.StreamHandler()  

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


async def connect_to_rabbitmq() -> aio_pika.RobustConnection: 

    for attempt in range(RABBIT_ATTEMPTS):
        try:
            connection = await aio_pika.connect_robust(
                RABBIT_CONN, timeout=5
            )
            logger.info("Connected to RabbitMQ!")
            return connection
        except aio_pika.exceptions.AMQPError as e:
            logger.warning(f"Attempt {attempt+1} failed (AMQPError): {e}")
            await asyncio.sleep(2)
        except Exception as e:
            logger.exception(f"Attempt {attempt+1} failed (General Error): {e}") 
            await asyncio.sleep(2)

    raise Exception("Failed to connect to RabbitMQ after multiple attempts")

@asynccontextmanager
async def lifespan(app: FastAPI):

    # async with async_engine.begin() as conn:
    #   await conn.run_sync(Base.metadata.create_all)

    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        print(f"Ошибка при применении миграций: {e}")

    app.rabbit_connection = await connect_to_rabbitmq()
    app.channel = await app.rabbit_connection.channel()
    

    # Очереди для общения с team service
    app.queue_to_team = await app.channel.declare_queue("user_to_team", durable=True)
    app.queue_from_team = await app.channel.declare_queue("user_email_from_team", durable=True)

    # Очереди для общения с task service
    app.queue_to_task = await app.channel.declare_queue("user_to_task", durable=True)
    app.queue_from_task = await app.channel.declare_queue("user_email_from_task", durable=True)

    # Очереди для общения с meeting service
    app.queue_to_meeting = await app.channel.declare_queue("user_to_meeting", durable=True)
    app.queue_from_meeting = await app.channel.declare_queue("user_email_from_meeting", durable=True)

    app.queue_to_org = await app.channel.declare_queue("user_to_organization", durable=True)
    app.queue_from_org = await app.channel.declare_queue("user_from_organization", durable=True)

    app.state.broker_producer_service = BrokerProducerService(app.channel)
    
    async def consume_team_messages():
        await app.queue_from_team.consume(get_broker_consumer_service().check_email_from_team)

    async def consume_task_messages():
        await app.queue_from_task.consume(get_broker_consumer_service().check_email_from_task)

    async def consume_meeting_messages():
        await app.queue_from_meeting.consume(get_broker_consumer_service().check_email_from_meeting)

    async def consume_org_messages():
        await app.queue_from_org.consume(get_broker_consumer_service().check_email_from_org)

    consumer_team_task = asyncio.create_task(consume_team_messages())
    consumer_task_task = asyncio.create_task(consume_task_messages())
    consumer_meeting_task = asyncio.create_task(consume_meeting_messages())
    consumer_org_task = asyncio.create_task(consume_org_messages())


    yield
    


    consumer_team_task.cancel()
    consumer_task_task.cancel()
    consumer_meeting_task.cancel()
    consumer_org_task.cancel()
    await asyncio.gather(consumer_team_task, consumer_task_task, consumer_meeting_task, consumer_org_task, return_exceptions=True) 

    await app.channel.close()


    await app.rabbit_connection.close()


    