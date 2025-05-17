from dataclasses import dataclass

from pik_smartbot.classes.Token import Token
from pik_smartbot.classes.User import User

@dataclass
class AccessControlService:

    #Прикрепляем токен

    def assign_token(self, user: User):
        if user.token is None or user.token.is_expired():
            new_token = Token()
            user.token = new_token
        else:
            return ValueError (f"Ошибка. У пользователя существует действительный токен {user.token}")


    def permission_token(self, User: User):



