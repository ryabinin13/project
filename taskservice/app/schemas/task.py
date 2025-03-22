from pydantic import BaseModel


class CreateTaskSchema(BaseModel):

    title: str
    discription: str