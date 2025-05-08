from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from pik_smartbot.classes import Departament, Workstation, Role, Position, Token, Car

@ dataclass
class User:
    id: int
    full_name: str
    birth_date: Optional[datetime] = None
    citizenship: Optional[str] = None #Гражданство
    owns_car: Optional[bool] = None #Наличие машины
    cars: Optional[List[Car]] = None
    departament: Optional[Departament] = None #Отдел сотрудника
    workstation: Optional[Workstation] = None
    role: Optional[Role] = None
    position: Optional[Position] = None
    probation_start: Optional[datetime] = None # дата начала испытательного срока
    token: Optional[Token] = None


    def is_on_probation(self) -> bool:
        if self.probation_start is None:
            return False
        return (datetime.now()-self.probation_start).days < 90

    def get_id(self) -> int:
        return self.id

    def get_full_name(self) -> str:
        return self.full_name
    def set_full_name(self, new_name: str):
        self.full_name = new_name

    def get_birth_day(self) -> datetime:
        return self.birth_date if self.birth_date else "Не указана"

    def _get_citizenship(self) -> str:
        return self.citizenship if self.citizenship else "Не указано"

    def get_role(self) -> str:
        return self.role if self.role else "Не назначена"

    def get_position(self) -> str:
        return self.position if self.position else "Не назначена"

    def add_car(self, car: Car):
        self.cars.append(car)
    def remove_car(self, numer_car: int):
        self.cars.remove(numer_car)
    def get_car(self) -> List[str]:
        return self.cars

    def get_departament(self) -> str:
        return self.departament
    def set_departament(self, departament: Departament):
        self.departament = departament

    def get_workstation(self) -> str:
        return self.workstation
    def set_workstation(self, workstation: Workstation):
        self.workstation = workstation

    def get_role(self) -> Role:
        return self.role






