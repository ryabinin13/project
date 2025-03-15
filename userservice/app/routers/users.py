from app.services.user import UserService
from config import config
from fastapi import APIRouter, Request, Response
from typing import Annotated
from fastapi import Depends
from app.dependencies import get_current_user, get_login_service, get_registration_service, get_user_service
from app.schemas.user import UserLoginSchema, UserRegistrationSchema, UserUpdateSchema
from app.services.login import LoginService
from app.services.registration import RegistrationService


user_router = APIRouter()

@user_router.post("/register")
async def registration(
    user_registration_schema: UserRegistrationSchema,
    registration_service: Annotated[RegistrationService, Depends(get_registration_service)]
    ):
    return await registration_service.registration(user_registration_schema)


@user_router.post("/login")
async def login(
    user_login_schema: UserLoginSchema,
    response: Response,
    request: Request,
    login_service: Annotated[LoginService, Depends(get_login_service)]
    ):
    return await login_service.login_user(user_login_schema, request, response)


@user_router.delete("/logout")
async def logout(
    response: Response
    ):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Вы вышли из системы"}


@user_router.put("/users/me")
async def update(
    user_update_chema: UserUpdateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)], 
    current_user_id: int = Depends(get_current_user)
    ):
    return await user_service.user_update(current_user_id, user_update_chema)


@user_router.delete("/users/me")
async def delete(
    user_service: Annotated[UserService, Depends(get_user_service)], 
    current_user_id: int = Depends(get_current_user)
    ):
    return await user_service.user_delete(current_user_id)