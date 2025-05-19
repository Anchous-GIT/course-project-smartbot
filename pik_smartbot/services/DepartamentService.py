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

    @staticmethod
    def workstation_verification(workstation: Workstation) -> None:
        if not isinstance(workstation, Workstation):
            raise ValueError("Место пользователя не является объектом класса Workstation")
        if not workstation.id:
            raise ValueError("Необходимо заполнить ID отдела")
        if not workstation.number:
            raise ValueError("Необходимо указать номер места пользователя")

    @staticmethod
    def workstation_update(workstation: Workstation) -> Workstation:
        DepartamentService.workstation_verification(workstation)

        logging.info(f"Updated workstation with ID {workstation.id}")
        return workstation

    @property
    def departaments(self) -> list[Departament]:
        return self._departaments

    @staticmethod
    def departament_verification(departament: Departament) -> None:
        if not isinstance(departament, Departament):
            raise ValueError("Передаваемый отдел пользователя не является объектом класса Departament")
        if not departament.id:
            raise ValueError("Необходимо заполнить ID отдела")
        if not departament.name:
            raise ValueError("Необходимо заполнить наименование отдела")

    @staticmethod
    def departament_update(departament: Departament) -> Departament:
        DepartamentService.departament_verification(departament)
        # TODO: Add a record to the database here (Добавить запись в базу данных здесь)
        pass
        logging.info(f"Updated departament with ID {departament.id}")
        return departament

    @staticmethod
    def is_duplicate_departament(departament: Departament, departaments: list[Departament]) -> bool:
        for d in departaments:
            if d.id == departament.id or d.name == departament.name:
                raise ValueError(f"Departament with ID {departament.id} already exists")
        return False

    def create_departament(self, id_departament: int, name: str) -> Departament:
        departament = Departament.create(id_departament, name)
        self.is_duplicate_departament(departament, self._departaments)
        self._departaments.append(departament)
        logging.info(f"Created departament '{name}' with ID {id_departament}")
        self.departament_update(departament)
        return departament

    def add_user_to_departament(self, departament: Departament, user: User) -> None:
        UserService.user_verification(user)
        self.departament_verification(departament)
        user.departament = departament
        UserService.update_user(user)

    def remove_user_from_departament(self, user: User) -> None:
        UserService.user_verification(user)
        user.departament = None
        UserService.update_user(user)

    def add_workstation_to_departament(self, departament: Departament, workstation: Workstation) -> Departament:
        self.departament_verification(departament)
        departament.add_workstation(workstation)
        self.departament_update(departament)
        return departament

    def create_workstation(self, departament: Departament, id_workstation: int, number: int, content: str = None) -> Workstation:
        DepartamentService.departament_verification(departament)
        workstation = Workstation.create(id_workstation, number, content)
        self.add_workstation_to_departament(departament, workstation)
        self.workstation_update(workstation)

    def remove_workstation_from_departament(self, departament: Departament, workstation: Workstation) -> Departament:
        self.departament_verification(departament)
        departament.remove_workstation(workstation)
        self.departament_update(departament)
        return departament

    def remove_workstation_from_departament_id(self, departament: Departament, id_workstation: int) -> Departament:
        self.departament_verification(departament)
        departament.remove_workstation_by_id(id_workstation)
        self.departament_update(departament)
        return departament

    def list_workstations_in_departament(self, departament: Departament) -> list[Workstation]:
        self.departament_verification(departament)
        return departament.workstations

    def assign_user_to_workstation(self, departament: Departament, workstation: Workstation, user: User) -> Workstation:
        self.departament_verification(departament)
        UserService.user_verification(user)


    def get_departament_by_id(self, id_departament: int) -> Optional[Departament]:
        if not isinstance(id_departament, int) or id_departament < 0:
            raise ValueError("Некорректный ID")
        for departament in self._departaments:
            if departament.id == id_departament:
                return departament