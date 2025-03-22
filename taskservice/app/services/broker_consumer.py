from uuid import uuid4, UUID 
from app.repositories.task import TaskRepository
from aio_pika.abc import AbstractIncomingMessage


class BrokerConsumerService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    
    async def task_add_user(self, message: AbstractIncomingMessage):
        async with message.process():
            message = message.body.decode()
            user_id, task_id = str(message).split()[-2:]
            user_id = UUID(user_id)

            task_id = int(task_id)

            task = await self.task_repository.get_id(task_id)
            if task:
                data = {"user_id": user_id}

                return await self.task_repository.update(task, data)
            
            return None