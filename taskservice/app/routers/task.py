from uuid import UUID
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user_id, get_task_service
from app.schemas.task import CreateTaskSchema
from app.services.task import TaskService

task_router = APIRouter()


@task_router.post("/tasks")
async def create_task(
    create_task_schema: CreateTaskSchema,
    task_service: TaskService = Depends(get_task_service)
    ):
    return await task_service.create_task(create_task_schema)


@task_router.post("/teams/{task_id}/users")
async def add_user(
    email: str,
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
    current_user_id: UUID = Depends(get_current_user_id)
    ):
    return await task_service.add_user(task_id, email)
