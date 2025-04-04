from fastapi import FastAPI
from app.database import Base, async_engine
from app.routers.users import user_router
from app.lifespan import lifespan
import uvicorn

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


async def create_database():
    async with async_engine.begin() as conn:
      await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_database()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


