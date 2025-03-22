from fastapi import FastAPI
from app.routers.marks import mark_router


app = FastAPI()
app.include_router(mark_router)