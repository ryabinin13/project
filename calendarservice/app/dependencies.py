from fastapi import HTTPException, Request
import jwt
from app.repositories.calendar import CalendarRepository
from app.services.broker_consumer import BrokerConsumerService
from app.services.calendar import CalendarService
from config import config
from app.database import get_async_session


async def get_calendar_repository() ->CalendarRepository:
    async with get_async_session() as session:
        return CalendarRepository(session=session)


async def get_calendar_service() -> CalendarService:
    from app.main import app
    calendar_repository= await get_calendar_repository()

    return CalendarService(calendar_repository=calendar_repository, app_state=app.state)


async def get_broker_consumer_service() -> BrokerConsumerService:
    from app.main import app
    calendar_repository= await get_calendar_repository()

    return BrokerConsumerService(calendar_repository=calendar_repository, app_state=app.state)

def get_current_user_id(request: Request):
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")

    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]) 
        user_id = payload.get("uid")
        if user_id is None:
            raise ValueError("Invalid token payload: 'uid' claim not found")
        if not isinstance(user_id, str):
            raise ValueError("Invalid token payload: 'uid' claim must be a string")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
