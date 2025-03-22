
from app.repositories.task import TaskRepository
from app.schemas.task import CreateTaskSchema


class TaskService:
    def __init__(self, repository: TaskRepository, app_state):
        self.task_repository = repository
        self.app_state = app_state


    async def create_task(self, create_task_schema: CreateTaskSchema):

        data = create_task_schema.model_dump()
        return await self.task_repository.create(data)


    async def add_user(self, task_id, email):
        await self.app_state.broker_producer_service.publish_add_user_in_task(task_id, email)
        