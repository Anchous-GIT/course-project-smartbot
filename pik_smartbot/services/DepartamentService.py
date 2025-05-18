from dataclasses import dataclass, field
from typing import Optional
import logging

from pik_smartbot.classes.User import  User
from pik_smartbot.classes.Departament import Departament
from pik_smartbot.classes.Workstation import Workstation
from pik_smartbot.services.UserService import UserService


@dataclass
class DepartamentService:
    _departaments: list[Departament] = field(default_factory=list)

    @property
    def departaments(self) -> list[Departament]:
        return self._departaments

    def new_departament(self, id_departament: int, name: str) -> Departament:
        if any(d.id == id_departament for d in self._departaments):
            raise ValueError(f"Departament with ID {id_departament} already exists.")
        departament = Departament(_id=id_departament, _name=name)
        self._departaments.append(departament)
        logging.info(f"Created departament '{name}' with ID {id_departament}")
        return departament

    def add_user_to_departament(self, departament: Departament, user: User) -> None:
        user.departament = departament
        UserService.update_user(user)

    def remove_user_from_departament(self, user: User) -> None:
        user.departament = None
        UserService.update_user(user)

    def add_workstation_to_departament(self, departament: Departament, workstation: Workstation) -> Departament:
        departament.add_workstation(workstation)
        return departament

    def remove_workstation_from_departament(self, departament: Departament, workstation: Workstation) -> Departament:
        departament.remove_workstation(workstation)
        return departament

    def remove_workstation_from_departament_id(self, departament: Departament, id_workstation: int) -> Departament:
        departament.remove_workstation_by_id(id_workstation)
        return departament

    def list_workstations_in_departament(self, departament: Departament) -> list[Workstation]:
        return departament.workstations

    def get_departament_by_id(self, id_departament: int) -> Optional[Departament]:
        for departament in self._departaments:
            if departament.id == id_departament:
                return departament
        return None
