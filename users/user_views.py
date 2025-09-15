
from fastapi import APIRouter

from users.sсhemas import CrateUser

from users import crud

router = APIRouter(prefix="/users",tags=["Users"])
@router.post("/")
async def create_users(user:CrateUser):
    return crud.createuser(user_in=user)