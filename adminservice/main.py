import sys
import os
from typing import Any, Dict
from sqladmin import Admin, ModelView
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from fastapi import FastAPI

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker



current_dir = os.path.dirname(os.path.abspath(__file__))

userservice_path = os.path.abspath(os.path.join(current_dir, '..'))

sys.path.insert(0, userservice_path)

from userservice.app.models.users import User
from teamservice.app.models.team import Team
from teamservice.app.models.team_memberships import TeamMemberships
from adminservice.config import DB_USER, DB_PORT, DB_PASS, DB_HOST
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]

class TeamAdmin(ModelView, model=Team):
    column_list = [Team.id]

class TeamMembershipsAdmin(ModelView, model=Team):
    column_list = [TeamMemberships.id]


app = FastAPI()

engines: Dict[str, Any] = {}
sessions: Dict[str, Any] = {}
bases: Dict[str, Any] = {}
admins: Dict[str, Admin] = {}  # Correctly type admins as a dictionary of Admin objects


databases = ["user_db"]

for db_name in databases:

    # app = FastAPI()

    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{db_name}"

    async_engine = create_async_engine(
        url=DATABASE_URL,
        echo=False
    )
    async_sessionmaker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    Base = declarative_base()

    engines[db_name] = async_engine
    sessions[db_name] = async_sessionmaker
    bases[db_name] = Base

    # admins[db_name] = Admin(app, async_engine) 

admin_user = Admin(app, engines["user_db"]) 
admin_user.add_view(UserAdmin)

