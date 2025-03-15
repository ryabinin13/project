from app.repositories.user import UserRepository
from app.schemas.user import UserUpdateSchema


class UserService:

    def __init__(self, repository: UserRepository):
        self.user_repository = repository

    
    async def user_update(self, current_user_id: int, user_update_schema: UserUpdateSchema):
        user = await self.user_repository.get_id(id=current_user_id)
        user_dict = {k: v for k, v in user_update_schema.model_dump().items() if v is not None}
        return await self.user_repository.update(user=user, data=user_dict)
    

    async def user_delete(self, current_user_id: int):
        return await self.user_repository.delete(current_user_id)