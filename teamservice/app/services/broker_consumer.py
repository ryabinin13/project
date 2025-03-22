from uuid import uuid4, UUID 
from app.repositories.team import TeamRepository
from app.repositories.team_memebership import TeamMembershipRepository
from aio_pika.abc import AbstractIncomingMessage


class BrokerConsumerService:
    def __init__(self, team_membership_repository: TeamMembershipRepository, team_repository: TeamRepository):
        self.team_membership_repository = team_membership_repository
        self.team_repository = team_repository

    
    async def team_membership_create(self, message: AbstractIncomingMessage):
        async with message.process():
            message = message.body.decode()
            user_id, team_id = str(message).split()[-2:]
            user_id = UUID(user_id)
            try:
                team_id = UUID(team_id)
            except:
                return None
            if await self.team_repository.get_id(team_id):
                data = {"team_id": team_id, "user_id": user_id}

                return await self.team_membership_repository.create(data)
            
            print("Такой команды не существует")
            return None