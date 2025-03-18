from fastapi import APIRouter

task_router = APIRouter()


@task_router.get("/test")
def test():
    return "hello"