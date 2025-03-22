from app.repositories.team import TeamRepository
from app.schemas.team import TeamCreateSchema


class TeamService:
    
    
    def __init__(self, repository: TeamRepository, app_state):
        self.team_repository = repository
        self.app_state = app_state


    async def team_create(self, team_create_schema: TeamCreateSchema):
        team_dict = team_create_schema.model_dump()
        return await self.team_repository.create(team_dict)
    

    async def add_user(self, team_id, email):
        await self.app_state.broker_producer_service.publish_add_user_in_task(team_id, email)