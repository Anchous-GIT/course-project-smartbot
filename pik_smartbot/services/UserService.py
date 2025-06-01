import logging
from dataclasses import dataclass
from datetime import datetime

from classes.Position import Position
from classes.Role import Role
from classes.User import User
from database.Database import db
from database.IdGeneration import id_gen
from enums.CitizenshipEnum import CitizenshipEnum


@dataclass
class UserService:

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
        db.update_user(user)
        logging.info(f"Updated user with ID {user.id}")
        return user

    def is_duplicate_user(self, user: User) -> bool:
        for u in db.users_list:
            if (u.id == user.id or u.telegram_id == user.telegram_id
                    or (u.full_name == user.full_name and u.birth_date == user.birth_date
                        and u.citizenship == user.citizenship)):
                raise ValueError(
                    f"Пользователь с такими данными уже существует:\n"
                    f"— ФИО: {u.full_name}\n"
                    f"— Дата рождения: {u.birth_date.strftime('%d.%m.%Y')}\n"
                    f"— Гражданство: {u.citizenship.value}\n\n"
                    f"Если это не ваша учетная запись, обратитесь к администратору.\n"
                    f"Ваш ID: {u.id}.")
        return False

    def create_user(self, telegram_id: int, full_name: str, birth_date: datetime, citizenship: CitizenshipEnum) -> User:
        user_id = id_gen.get_next_user_id()
        user = User.create(user_id, telegram_id, full_name, birth_date, citizenship)
        self.is_duplicate_user(user)
        db.add_user(user)
        logging.info(f"Created user with ID {user_id}")
        self.update_user(user)
        return user

    def remove_user(self, user: User) -> None:
        self.user_verification(user)
        db.remove_user(user)
        logging.info(f"Removed user with ID {user.id}")

    def update_telegram_id(self, user: User, telegram_id: int) -> User:
        self.user_verification(user)
        user.telegram_id = telegram_id
        self.is_duplicate_user(user)
        self.update_user(user)
        return user

    def rename(self, user: User, full_name: str) -> User:
        self.user_verification(user)
        user.full_name = full_name
        self.update_user(user)
        return user

    def change_user_role(self, user: User, role: Role):
        self.user_verification(user)
        user.role = role

    def change_user_position(self, user: User, position: Position ):
        self.user_verification(user)
        user.position = position

    def change_citizenship(self, user: User, citizenship: CitizenshipEnum):
        self.user_verification(user)
        user.citizenship = citizenship



