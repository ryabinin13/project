from app.message_broker import MessageBroker
from app.repositories.user import UserRepository
from app.schemas.user import UserRegistrationSchema
from werkzeug.security import generate_password_hash
from exeptions import UserAlreadyHasEmailException


class RegistrationService:

    def __init__(self, repository: UserRepository, message_broker: MessageBroker):
        self.user_repository = repository
        self.message_broker = message_broker


    async def registration(self, user_registration_schema: UserRegistrationSchema):
        user = await self.user_repository.get_email(email=user_registration_schema.email)
        if user:
            return UserAlreadyHasEmailException
        
        team_id = user_registration_schema.team_id
        password_hash = generate_password_hash(user_registration_schema.password1)
        user_dict = user_registration_schema.model_dump(exclude=["password2", "password1", "team_id"])
        user_dict["password_hash"] = password_hash

        id = await self.user_repository.create(user_dict)
        await self.message_broker.publish_user_registered(str(id) + " " + team_id)
        return id