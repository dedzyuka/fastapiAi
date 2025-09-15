from users.sсhemas import CrateUser


def createuser(user_in:CrateUser)->dict:
    user = user_in.model_dump()
    return{"success": True,
           "user":user}