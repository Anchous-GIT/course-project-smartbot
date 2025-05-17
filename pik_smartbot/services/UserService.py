from dataclasses import dataclass

from pik_smartbot.classes import User
from pik_smartbot.dto import UserRegistrationDTO


@dataclass
class UserService:

    def create_user(self, user_date: UserRegistrationDTO) -> User:
        user = User
        user.full_name = user_date.full_name
        user.birth_date = user_date.birth_date
        user.citizenship = user_date.citizenship
        user.own_car = user_date.own_car
        user.department = user_date.department
        return user

    def update_user(self, user: User, user_date: UserRegistrationDTO) -> User:
        user.full_name = user_date.full_name
        user.birth_date = user_date.birth_date





