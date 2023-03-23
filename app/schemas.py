from datetime import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    email: str


class UserCreateSchema(UserSchema):
    password: str


class UserResponseSchema(UserSchema):
    id: int
    created_at: datetime

    class Config:
        """Config for UserResponseSchema"""

        orm_mode = True
