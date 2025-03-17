from app.repositories.team import TeamRepository
from app.schemas.team import TeamCreateSchema


class TeamService:
    
    
    def __init__(self, repository: TeamRepository):
        self.team_repository = repository


    async def team_create(self, team_create_schema: TeamCreateSchema):
        team_dict = team_create_schema.model_dump()
        return await self.team_repository.create(team_dict)