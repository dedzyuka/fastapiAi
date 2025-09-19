from fastapi import APIRouter, Depends


from sqlalchemy.ext.asyncio import AsyncSession

from users.sсhemas import CrateUser


from chat.schemas import NewChat
from fChat.fun import newChat

from DBconn.db import db_helper

router = APIRouter(prefix="/chat",tags=["chat"])
@router.post("/")
async def create_chat(chat:NewChat, user:CrateUser):
    from chat.crud import newchatCrud
    resp = newchatCrud(newchat=chat,user=user)
    return resp

@router.post("/test")
async def testR(
    newchat: NewChat,
    user: CrateUser,
    session: AsyncSession = Depends(db_helper.session_getter)  # FastAPI внедряет сессию
):
    from chat.crud import testing
    resp = await testing(chat=newchat, user=user, session=session)
    return resp

@router.post("/newchat")
async def create_chat_endpoint(
    newchat: NewChat,
    user: CrateUser,
    session: AsyncSession = Depends(db_helper.session_getter)
):
    from chat.crud import create_new_chat
    resp = await create_new_chat(newchat=newchat, user=user, session=session)
    return resp