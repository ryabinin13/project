from fastapi import HTTPException, Request
import jwt
from app.repositories.team import TeamRepository
from app.database import get_async_session
from app.repositories.team_memebership import TeamMembershipRepository
from app.services.consumer import ConsumerService
from app.services.team import TeamService
from config import config


def get_team_membership_repository() ->TeamMembershipRepository:
    return TeamMembershipRepository(session=get_async_session())

def get_team_repository() ->TeamRepository:
    return TeamRepository(session=get_async_session())

def get_team_service() -> TeamService:
    return TeamService(repository=get_team_repository())

def get_consumer_service() -> ConsumerService:
    return ConsumerService(team_membership_repository=get_team_membership_repository(), team_repository=get_team_repository())



def get_current_user_id(request: Request):
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")

    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]) 
        user_id = payload.get("uid")
        if user_id is None:
            raise ValueError("Invalid token payload: 'uid' claim not found")
        return int(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")