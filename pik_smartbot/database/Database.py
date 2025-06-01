import json
import os
from dataclasses import dataclass, field
from typing import List, Optional

from httpx import request

from classes.Departament import Departament
from classes.Position import Position
from classes.Request import Request
from classes.Role import Role
from classes.User import User
from database.IdGeneration import id_gen


@dataclass
class Database:
    users: List[User] = field(default_factory=list)
    requests: List[Request] = field(default_factory=list)
    departaments: List[Departament] = field(default_factory=list)
    positions: List[Position] = field(default_factory=list)
    roles: List[Role] = field(default_factory=list)

    # noinspection PyTypeChecker
    def save_to_file(self, path: str = "database.json"):
        temp_path = path + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump({
                "users": [u.to_dict() for u in self.users],
                "requests": [r.to_dict() for r in self.requests],
                "departaments": [d.to_dict() for d in self.departaments],
                "roles": [rl.to_dict() for rl in self.roles],
                "positions":[p.to_dict() for p in self.positions]
            }, file, ensure_ascii=False, indent=4)
        os.replace(temp_path, path)

    def load_from_file(self, path: str = "database.json"):
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.users = [User.from_dict(u) for u in data.get("users", [])]
            self.requests = [Request.from_dict(r) for r in data.get("requests", [])]
            self.departaments = [Departament.from_dict(d) for d in data.get("departaments", [])]
            self.roles = [Role.from_dict(rl) for rl in data.get("roles", [])]
            self.positions = [Position.from_dict(p) for p in data.get("positions", [])]
            max_user_id = max((user.id for user in self.users), default=0)
            max_request_id = max((request_.id for request_ in self.requests), default=0)
            max_roles_id = max((role.id for role in self.departaments), default=0)
            max_departaments_id = max((departament.id for departament in self.departaments), default=0)
            max_positions_id = max((position.id for position in self.positions), default=0)


            id_gen.set_start_ids(
                user_id=max_user_id,
                request_id=max_request_id,
                role_id=max_roles_id,
                position_id=max_positions_id,
                departament_id=max_departaments_id,
                workstation_id=0
                #TODO:добавить к остальным также вычисление максимального айди
            )

        except FileNotFoundError:
            pass




    def update_user(self, user: User) -> None:
        for i, u in enumerate(self.users):
            if u.id == user.id:
                self.users[i] = user
                self.save_to_file()
                return
        raise ValueError(f"User with id {user.id} not found")

#"""----------------------------------------------------------------------------"""
    def add_departament(self, departament: Departament) -> None:
        self.departaments.append(departament)
        db.save_to_file()

    def remove_departament(self, departament: Departament) -> None:
        self.departaments.remove(departament)
        self.save_to_file()

    def get_departament_by_name(self, name: str) -> Departament | None:
        for departament in self.departaments:
            if departament.name == name:
                return departament
        return None

    def get_departament_by_id(self, id_departament: int) -> Departament | None:
        for departament in self.departaments:
            if departament.id == id_departament:
                return departament

    def get_departaments_list(self) -> List[Departament]:
        return self.departaments

    def is_duplicate_departament(self, departament: Departament) -> bool:
        for d in self.departaments:
            if d.id == departament.id or d.name == departament.name:
                raise ValueError(f"Departament with ID {departament.id} already exists")
        return False
#"""----------------------------------------------------------------"""
    def get_position_by_name(self, name: str) -> Position | None:
        for position in self.positions:
            if position.name == name:
                return position
        return None

    def add_position(self, position: Position) -> None:
        self.positions.append(position)
        self.save_to_file()

    def add_role(self, role: Role) -> None:
        self.roles.append(role)
        self.save_to_file()









#"""------------------------------------------------------------------------"""
    def add_user(self, user: User) -> None:
        self.users.append(user)
        self.save_to_file()

    def add_request(self, request: Request) -> None:
        self.requests.append(request)
        self.save_to_file()

    def remove_user(self, user: User) -> None:
        self.users.remove(user)
        self.save_to_file()

    def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        for user in self.users:
            if user.telegram_id == telegram_id:
                return user
        return None

    @property
    def users_list(self):
        return self.users

    @property
    def requests_list(self):
        return self.requests

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        if not isinstance(user_id, int) or user_id < 0:
            raise ValueError("Некорректный ID")
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def get_request_by_id(self, id_request: int):
        if not isinstance(id_request, int) or id_request < 0:
            raise ValueError("Некорректный ID")
        for request in self.requests:
            if request.id == id_request:
                return request
        raise ValueError("Заявка не найдена")


db = Database()
db.load_from_file()


