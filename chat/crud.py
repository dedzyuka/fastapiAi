from fChat.fun import newChat, test
from users.sсhemas import CrateUser
from chat.schemas import NewChat,Chat
def newchatCrud(newchat:NewChat, user:CrateUser):
    from fChat.fun import newChat
    resp = newChat(newchat,user)
    return resp
def testing(newchat:Chat, user:CrateUser):
    req = test(history = newchat, user=user)
    return req