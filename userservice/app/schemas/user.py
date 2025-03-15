from typing import Optional, Self
from pydantic import BaseModel, model_validator, Field


class UserRegistrationSchema(BaseModel):

    username: str = Field(min_length=3)
    email: str
    password1: str = Field(min_length=6)
    password2: str = Field(min_length=6)

    @model_validator(mode='after')
    def check_password(self)-> Self:
        if self.password1 != self.password2:
            raise ValueError("Пароли не совпадают")
        return self
    

class UserUpdateSchema(BaseModel):
    username: str = Field(default=None)
    email: str = Field(default=None)
    password: str = Field(default=None)


class UserLoginSchema(BaseModel):
    email: str
    password: str