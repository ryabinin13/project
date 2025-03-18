from fastapi import APIRouter, Depends

from app.dependencies import get_team_service, get_current_user_id
from app.schemas.team import TeamCreateSchema
from app.services.team import TeamService
from app.schemas.user import AddUserSchema


team_router = APIRouter()


@team_router.post("/teams")
async def team_create(
    team_create_schema: TeamCreateSchema,
    team_service: TeamService = Depends(get_team_service),
    current_user_id: int = Depends(get_current_user_id)
    ):
    return await team_service.team_create(team_create_schema)


@team_router.post("/teams/{team_id}/users")
async def add_user(add_user_schema: AddUserSchema):
    pass


