from dataclasses import dataclass
import logging

from classes.Departament import Departament
from classes.User import User
from classes.Workstation import Workstation
from database.Database import db
from database.IdGeneration import id_gen
from services.UserService import UserService


@dataclass
class DepartamentService:

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
        #TODO: добавить запись в бд
        logging.info(f"Updated workstation with ID {workstation.id}")
        return workstation

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


    def create_departament(self, name: str) -> Departament:
        departament = Departament.create(name)
        db.is_duplicate_departament(departament)
        db.add_departament(departament)
        logging.info(f"Created departament '{name}' with ID {departament.id}")
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

    def create_workstation(self, departament: Departament, number: int, content: str = None) -> Workstation:
        DepartamentService.departament_verification(departament)
        workstation = Workstation.create(number, content)
        self.add_workstation_to_departament(departament, workstation)
        self.workstation_update(workstation)
        return workstation

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

    def assign_user_to_workstation(self, workstation: Workstation, user: User) -> Workstation:
        self.workstation_verification(workstation)
        UserService.user_verification(user)
        user.workstation = workstation
        return self.workstation_update(workstation)

