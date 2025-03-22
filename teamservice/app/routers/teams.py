from fastapi import APIRouter, Depends

from app.dependencies import get_team_service, get_current_user_id
from app.schemas.team import TeamCreateSchema
from app.services.team import TeamService
from uuid import UUID

team_router = APIRouter()


@team_router.post("/teams")
async def team_create(
    team_create_schema: TeamCreateSchema,
    team_service: TeamService = Depends(get_team_service),
    current_user_id: UUID = Depends(get_current_user_id)
    ):
    return await team_service.team_create(team_create_schema)


@team_router.post("/teams/{team_id}/users")
async def add_user(
    email: str,
    team_id: UUID,
    team_service: TeamService = Depends(get_team_service),
    current_user_id: UUID = Depends(get_current_user_id)
    ):
    return await team_service.add_user(team_id, email)


