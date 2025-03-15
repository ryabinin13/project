from app.repositories.user import UserRepository
from app.schemas.user import UserRegistrationSchema
from werkzeug.security import generate_password_hash
from exeptions import UserAlreadyHasEmailException


class RegistrationService:

    def __init__(self, repository: UserRepository):
        self.user_repository = repository


    async def registration(self, user_registration_schema: UserRegistrationSchema):
        user = await self.user_repository.get_email(email=user_registration_schema.email)
        if user:
            return UserAlreadyHasEmailException
        password_hash = generate_password_hash(user_registration_schema.password1)
        user_dict = user_registration_schema.model_dump(exclude=["password2", "password1"])
        user_dict["password_hash"] = password_hash
        return await self.user_repository.create(user_dict)