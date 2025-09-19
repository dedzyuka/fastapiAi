from typing import Annotated

from contextlib import asynccontextmanager

from fastapi import FastAPI ,HTTPException,Path
from typing import Optional

from DBconn.db import db_helper
import uvicorn


from users.user_views import router as users_router

from chat.chat_view import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    print("dispose engine")
    await db_helper.dispose()



mainapp = FastAPI(lifespan=lifespan)
mainapp.include_router(users_router)

mainapp.include_router(chat_router)


@mainapp.get("/")
async def home()-> dict[str,str]:
    return {"data":"value"}



if __name__ == "__main__":
    uvicorn.run("main:mainapp",reload=True)