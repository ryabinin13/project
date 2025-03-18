from fastapi import FastAPI
from app.routers.task import task_router

app = FastAPI()
app.include_router(task_router)