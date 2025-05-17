from dataclasses import dataclass

from pik_smartbot.classes.Token import Token
from pik_smartbot.classes.User import User
from pik_smartbot.enums.PermissionsEnum import PermissionsEnum


@dataclass
class AccessControlService:
    # Назначить новый токен, если его нет или он просрочен
    def assign_token(self, user: User) -> None:
        if user.token is None or user.token.is_expired():
            user.token = Token()
        else:
            raise ValueError(f"У пользователя уже есть действительный токен: {user.token.token}")

    # Добавить разрешение к токену пользователя
    def add_permission_token(self, user: User, permission: PermissionsEnum) -> bool:
        if user.token:
            return user.token.add_permission(permission)
        raise ValueError("Пользователь не имеет назначенного токена")

    # Удалить разрешение из токена пользователя
    def remove_permission_token(self, user: User, permission: PermissionsEnum) -> bool:
        if user.token:
            return user.token.remove_permission(permission)
        raise ValueError("Пользователь не имеет назначенного токена")

    # Проверить, содержит ли токен пользователя определенное разрешение
    def check_permission_token(self, user: User, permission: PermissionsEnum) -> bool:
        if user.token:
            return user.token.check_permission(permission)
        return False
