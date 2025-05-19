import datetime
import logging
from dataclasses import dataclass, field

from pik_smartbot.classes.User import User
from pik_smartbot.enums.CitizenshipEnum import CitizenshipEnum

"""Добавить на прием инф-ии UserRegistrationDTO"""
@dataclass
class UserService:
    _users: list[User] = field(default_factory=list)

    @property
    def users(self) -> list[User]:
        return self._users

    @staticmethod
    def user_verification(user: User) -> None:
        if not isinstance(user, User):
            raise ValueError("Пользователь не является объектом класса User")
        if not user.id:
            raise ValueError("Необходимо заполнить ID пользователя")
        if not user.telegram_id:
            raise ValueError("Необходимо заполнить ID telegram пользователя")
        if not user.full_name:
            raise ValueError("Необходимо заполнить ФИО пользователя")
        if not user.citizenship:
            raise ValueError("Необходимо указать гражданство пользователя")

    @staticmethod
    def update_user(user: User) -> User:
        UserService.user_verification(user)
        # TODO: Add a record to the database here (Добавить запись в базу данных здесь)
        pass
        logging.info(f"Updated user with ID {user.id}")
        return user

    @classmethod
    def is_duplicate_user(cls, user: User, users: list[User]) -> bool:
        for u in users:
            if (u.id == user.id or u.telegram_id == user.telegram_id
                    or (u.full_name == user.full_name and u.birth_date == user.birth_date
                        and u.citizenship == user.citizenship)):
                raise ValueError(f"User with similar data already exists: {user}")
        return False

    def create_user(self, user_id: int, telegram_id: int, full_name: str,birth_date: datetime, citizenship: CitizenshipEnum) -> User:
        user = User.create(user_id, telegram_id, full_name, birth_date, citizenship)
        self.is_duplicate_user(user, self.  _users)
        self._users.append(user)
        logging.info(f"Created user with ID {user_id}")
        self.update_user(user)
        return user

    def update_telegram_id(self, user: User, telegram_id: int) -> User:
        self.user_verification(user)
        user.telegram_id = telegram_id
        self.is_duplicate_user(user, self._users)
        self.update_user(user)
        return user

    def rename_user(self, user: User, full_name: str) -> User:
        self.user_verification(user)
        user.full_name = full_name
        self.update_user(user)
        return user



