from dotenv import load_dotenv, find_dotenv

from langchain.memory import ConversationSummaryMemory
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.chains import ConversationChain

from langchain.schema import (AIMessage, HumanMessage, SystemMessage)

from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate

from pgvector.psycopg2 import register_vector
from sqlalchemy import update, insert

from chat.schemas import NewChat
from users.sсhemas import CrateUser

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from DBconn.db import db_helper
import asyncpg
import os
from models.models import Chat
from chat.schemas import NewChat



# def req_resp(chat:Chat):
#     conn = psycopg2.connect(
#     dbname="vectordb",
#     user="postgres",
#     password="password123",
#     host="localhost",
#     port=5433
#     )   
#     register_vector(conn)

#     cur = conn.cursor()
#     query_embedding = encodeToSendInDB(text_query)
#     sql = """
#     SELECT id, text, embedding <-> %s::vector AS distance
#     FROM embeddings
#     ORDER BY distance
#     LIMIT %s;
#     """
#     cur.execute(sql, (query_embedding, top_k))
#     results = cur.fetchall()
#     resp = []
#     for r in results:
#         resp.append(f"id: {r[0]}, text: ///, distance: {r[2]}")

#     cur.close()
#     conn.close()

#     chat = ChatGoogleGenerativeAI(model = "gemini-2.0-flash", temperature = 0.3)

#     memory = ConversationSummaryMemory(llm=chat)
#     conversation = ConversationChain(llm=chat, memory=memory, verbose=True)
#     conversation.run(s)
#     conversation.




async def newChat(newChat: NewChat, user: CrateUser):
    load_dotenv(find_dotenv())

    chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
    memory = ConversationSummaryMemory(llm=chat)
    conversation = ConversationChain(llm=chat, memory=memory, verbose=True)
    
    resp = conversation.run(newChat.newReq)

    conn = await asyncpg.connect(
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password123"),
        database=os.getenv("DB_NAME", "vectordb"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 5433))
    )
    
    user_id = user.user_id
    sumnchat = f"{memory.buffer}"

    sql = """
    INSERT INTO messages (user_id, sumnchat) 
    VALUES ($1, $2)
    RETURNING id;
    """
    new_chat_id = await conn.fetchval(sql, user_id, sumnchat)
    
    await conn.close()

    print(f"Создан чат с id: {new_chat_id} для пользователя: {user_id}")
    return {"success": True, "user": resp}



async def get_sumnchat(chat_id: int, session: AsyncSession) -> str:
    result = await session.execute(select(Chat).where(Chat.id == chat_id))
    chat = result.scalars().first()
    if chat is None:
        raise ValueError("Chat not found")
    return chat.sumnChat


async def update_sumnchat(
    new_sumn: str,
    chat_id: int,
    session: AsyncSession = Depends(db_helper.session_getter)  # без скобок
) -> str:
    """
    Обновляет строку sumnchat для указанного chat_id.
    """
    stmt = (
        update(Chat)  # Здесь Chat — это ORM класс модели, например from yourapp.models import Chat
        .where(Chat.id == chat_id)  # Обратите внимание на имя поля pk, обычно это id
        .values(sumnChat=new_sumn)
    )
    await session.execute(stmt)
    await session.commit()
    return "success"

async def newChatDB(new_sumn: str, user: CrateUser, session: AsyncSession):
    stmt = (
        insert(Chat)
        .values(
            user_id=user.user_id,            # <--- Добавьте это!
            founder_username=user.username,
            sumnChat=new_sumn
        )
    )
    await session.execute(stmt)
    await session.commit()
    return "success"
