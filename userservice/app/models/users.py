from typing import Optional
from sqlalchemy import Date, Integer, Sequence, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import date


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]
    birthday: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True) 