from pik_smartbot.classes.Token import Token
from pik_smartbot.classes.User import User

class AccessControlService:

    def assign_token(self, user: User):
        if user.token is None or user.token.is_expired():
            new_token = Token()
            user.token = new_token


