from fastapi import FastAPI
from app.routers.users import user_router
from app.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


