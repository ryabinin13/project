from contextlib import asynccontextmanager
from app.routers.users import user_router
from aio_pika import connect, connect_robust
from fastapi import FastAPI
from config import RABBIT_CONN


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = await connect_robust(RABBIT_CONN)
    channel = await connection.channel()
    await channel.declare_queue(
            "user_registered",
            durable=True)
    print("Consumer App started")
    yield
    print("Consumer App stopped")

    