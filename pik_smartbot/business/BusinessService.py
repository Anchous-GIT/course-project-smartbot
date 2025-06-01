from dataclasses import dataclass
from datetime import datetime
from typing import Any

from classes.Position import Position
from classes.Role import Role
from classes.User import User
from database.Database import db
from enums.CitizenshipEnum import CitizenshipEnum
from enums.RequestEnum import RequestEnum
from services.AccessControlService import AccessControlService
from services.DepartamentService import DepartamentService
from services.RequestService import RequestService
from services.UserService import UserService


@dataclass
class BusinessService:
    user_svc: UserService
    request_svc: RequestService
    department_svc: DepartamentService
    acs_svc: AccessControlService

    """Работа с пользователями----------------------------------------------------------------------------------------------"""

    """Регистрация пользователя, команда /register"""
    def register_user(self, telegram_id: int, full_name: str,birth_date: datetime, citizenship: CitizenshipEnum):
        user = self.user_svc.create_user(telegram_id, full_name, birth_date, citizenship)
        #TODO: добавить реализация отправки уведомления начальнику отдела и администратору
        return user

    """Возвращает информацию по пользователю, команда /profile"""
    def get_profile_data(self, telegram_id: int) -> str:
        user = db.get_user_by_telegram_id(telegram_id)
        if not user:
            raise ValueError("Пользователь не найден")
        #TODO: добавить вывод заявок при необходимости, возможность их отменить(может быть)
        return (
            f"👤 *Ваш профиль:*\n"
            f"🆔 Telegram ID: `{user.telegram_id}`\n"
            f"📛 Имя: {user.full_name}\n"
            f"🎂 Дата рождения: {user.birth_date.strftime('%d.%m.%Y')}\n"
            f"🌍 Гражданство: {user.citizenship.value}\n"
            f"📌 Роль: {user.role.name.value if user.role else 'Не назначена'}\n" 
            f"💼 Должность: {user.position.name.value if user.position else 'Не назначена'}\n"
            f"🏢 Отдел: {user.departament if user.departament else 'Не назначен'}"
        )

    """Редактирование профиля (фио, отдел, должность, гражданство, дату рождения, и тд, команда /edit_profile"""
    def update_user_profile(self, user_id: int, updates: dict[str, Any]) -> User:
        user = db.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")

        for attr, value in updates.items():
            match attr:
                case "position":
                    try:
                        position = db.get_position_by_name(value)
                        if position is None:
                            position = Position.create(value)
                            db.add_position(position)
                            print(
                                f"Position '{value}' created successfully.")  # Заменить на logger.info при необходимости
                        self.user_svc.change_user_position(user, position)
                    except Exception as e:
                        raise ValueError(f"❌ Failed to process position '{value}': {str(e)}")
                case "role":
                    try:
                        role = Role.create(value)
                        self.user_svc.change_user_role(user, role)
                    except Exception as e:
                        raise ValueError(f"Role '{value}' not found: {str(e)}")
                case "department":
                    department = db.get_department_by_name(value)
                    if department is None:
                        raise ValueError(f"Department '{value}' not found.")
                    self.department_svc.add_user_to_departament(user, department)
                case "citizenship":
                    try:
                        citizenship = CitizenshipEnum(value)
                        self.user_svc.change_citizenship(user, citizenship)
                    except ValueError:
                        raise ValueError(f"Invalid citizenship value: '{value}'")
                case "full_name" | "birth_date" | "workstation_number":
                    setattr(user, attr, value)
                case _:
                    raise ValueError(f"Unknown attribute '{attr}'")

        self.user_svc.update_user(user)
        return user


    """Работа с заявками------------------------------------------------------------------------------------------------"""
    def create_request(self, user: User, request_type: RequestEnum, value_request:str):
        #TODO: добавить уведомления, рассылку по нужным адресам
        return self.request_svc.create_request(user, request_type, value_request)




