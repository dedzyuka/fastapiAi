from pydantic import BaseModel, Field
from typing import Optional
from typing import Annotated
from annotated_types import MaxLen,MinLen

class NewChat(BaseModel):
    founder_username: Annotated[str, MinLen(3), MaxLen(20)]
    newReq: str

class ChatOut(NewChat):
    id: int
    sumnChat: Optional[str] = None

    class Config:
        from_attributes = True