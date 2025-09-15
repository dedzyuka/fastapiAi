from typing import Annotated

from fastapi import FastAPI ,HTTPException,Path
from typing import Optional
import uvicorn


from users.user_views import router as users_router

from chat.chat_view import router as chat_router

app = FastAPI()
app.include_router(users_router)

app.include_router(chat_router)


@app.get("/")
async def home()-> dict[str,str]:
    return {"data":"value"}



if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)