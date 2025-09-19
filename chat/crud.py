from fastapi import Depends
from fChat.fun import get_sumnchat, update_sumnchat, newChatDB
from users.sсhemas import CrateUser
from chat.schemas import NewChat
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from DBconn.db import db_helper

from langchain.memory import ConversationSummaryBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain


def newchatCrud(newchat:NewChat, user:CrateUser):
    from fChat.fun import newChat
    resp = newChat(newchat,user)
    return resp



async def testing(
    chat: NewChat,
    user: CrateUser,
    session: AsyncSession,
):
    sumnchat_value = await get_sumnchat(chat.id, session = session)

    # Создаем чат на основе модели
    chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

    # Инициализация памяти разговора
    memory = ConversationSummaryBufferMemory(llm=chat)
    memory.buffer = sumnchat_value

    # Создаем цепочку общения с памятью
    conversation = ConversationChain(llm=chat, memory=memory, verbose=True)

    req = chat.newReq

    # Если run - синхронный, заменяем на асинхронный вызов arun
    resp = await conversation.run(req)  # используем await здесь

    return {
        "success": True,
        "resp": resp,
        "memory_buffer": memory.buffer
    }

async def create_new_chat(user:CrateUser, newchat:NewChat, session: AsyncSession):
    load_dotenv(find_dotenv())
    chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

    # Инициализация памяти разговора
    memory = ConversationSummaryBufferMemory(llm=chat)

    # Создаем цепочку общения с памятью
    conversation = ConversationChain(llm=chat, memory=memory, verbose=True)

    req = newchat.newReq

    # Если run - синхронный, заменяем на асинхронный вызов arun
    resp = await conversation.arun(req)
    mem = memory.buffer
    a = await newChatDB(new_sumn = mem, user=user,session = session)

    

    return {
        "success": True,
        "resp": resp,
        "memory_buffer": memory.buffer,
        "db_success": a
    }

