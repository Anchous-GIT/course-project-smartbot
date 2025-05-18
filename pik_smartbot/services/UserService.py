import logging
from dataclasses import dataclass, field

from pik_smartbot.classes.User import User
from pik_smartbot.enums.CitizenshipEnum import CitizenshipEnum

"""Добавить на прием инф-ии UserRegistrationDTO"""
@dataclass
class UserService:
    _users: list[User] = field(default_factory=list)

    def user_verification(self, user: User) -> bool:
        if not isinstance(user, User):
            raise ValueError("Пользователь не является объектом класса User")
        return True

    def create_user(self, user_id: int, telegram_id: int, full_name: str, citizenship: CitizenshipEnum) -> User:
        user = User(_id = user_id, _telegram_id = telegram_id, _full_name = full_name, _citizenship = citizenship)
        self._users.append(user)
        logging.info(f"Created user with ID {user_id}")
        return user

    def update_telegram_id(self, user: User, telegram_id: int) -> User:
        if self.user_verification(user):
            user.telegram_id = telegram_id
            logging.info(f"Updated Telegram ID for user with ID {user.id} to {telegram_id}")
        return user

    def rename_user(self, user: User, full_name: str):
        self.user_verification(user)
        user.full_name = full_name
        logging.info(f"Renamed user with ID {user.id} to {full_name}")


    
    

    #Настроить на обновление все инфы в бд
    def update_user(user: User) -> User:
       metod = "пустышка"





