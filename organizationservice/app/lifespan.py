import asyncio
from contextlib import asynccontextmanager
import os
from aio_pika import connect, connect_robust
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

    app.queue_from_team = await app.channel.declare_queue("team_to_organization", durable=True)
    app.queue_to_team = await app.channel.declare_queue("team_from_organization", durable=True)

    app.queue_from_user = await app.channel.declare_queue("user_to_organization", durable=True)
    app.queue_to_user = await app.channel.declare_queue("user_from_organization", durable=True)

    app.state.broker_producer_service = BrokerProducerService(app.channel)

    async def consume_team_messages():
        await app.queue_from_team.consume(get_broker_consumer_service().org_create)
    consumer_team_task = asyncio.create_task(consume_team_messages())
    
    async def consume_user_messages():
        await app.queue_from_user.consume(get_broker_consumer_service().org_membership_create)
    consumer_user_task = asyncio.create_task(consume_user_messages())
    
    yield



    consumer_team_task.cancel()
    consumer_user_task.cancel()
    await asyncio.gather(consumer_user_task, consumer_team_task, return_exceptions=True) 

    await app.channel.close()


    await app.rabbit_connection.close()