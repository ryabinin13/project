from fastapi import APIRouter


mark_router = APIRouter()


@mark_router.post("/marks")
async def create_mark():
    pass