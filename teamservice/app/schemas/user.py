from pydantic import BaseModel



class AddUserSchema(BaseModel):

    email: str