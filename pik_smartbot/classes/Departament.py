from dataclasses import dataclass, field
from typing import List
from pik_smartbot.classes import User
from pik_smartbot.classes.Workstation import Workstation

#Даем возможность менять имя отдела, добавлять/удалять сотрудников и рабочие места
@ dataclass
class Departament:
    _id_departament: int
    _name_departament: str

    _users: List["User"] = field(default_factory=list)
    _workstations: List["Workstation"] = field(default_factory=list)

    @property
    def id_departament(self)-> int:
        return self._id_departament

    @property
    def name_departament(self) -> str:
        return self._name_departament

    @name_departament.setter
    def name_departament(self,name_departament:str):
        self._name_departament = name_departament

    @property
    def users(self)-> list[User]:
        return self._users

    @property
    def workstations(self)-> list[Workstation]:
        return self._workstations

    def add_user(self, users: User):
        self._users.append(users)

    def remove_user(self, id_user: int):
        for user in self._users:
            if user.id == id_user:
                self._users.remove(user)
                return
        raise ValueError(f"Сотрудник с ID {id_user} не найден.")

    def add_workstation(self, workstation: Workstation):
        self._workstations.append(workstation)

    def remove_workstation(self, id_workstation: int):
        for workstation in self._workstations:
            if workstation.id == id_workstation:
                self._workstations.remove(workstation)
                return
        raise ValueError(f"Место с ID {id_workstation} не найдено.")

