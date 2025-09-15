from pydantic import BaseModel

from typing import Annotated
from annotated_types import MaxLen,MinLen


class CrateUser(BaseModel):
    user_id: int
    username: Annotated[str, MinLen(3), MaxLen(20)]

class PublicUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]

class UserCreate(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: str
    class Config:
        from_attributes = True