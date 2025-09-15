from fastapi import APIRouter


from chat.crud import newchatCrud,testing

from users.shemas import CrateUser


from chat.schemas import NewChat, Chat
from fChat.fun import newChat

router = APIRouter(prefix="/chat",tags=["chat"])
@router.post("/")
async def create_chat(chat:NewChat, user:CrateUser):
    resp = newchatCrud(newchat=chat,user=user)
    return resp

@router.post("/test")
async def testR(newchat:Chat, user:CrateUser):
    resp = testing(newchat=newchat, user= user)
    return resp