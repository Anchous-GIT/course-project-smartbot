from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from pik_smartbot.classes import Departament, Workstation, Position, Token, Car, Role
from pik_smartbot.enums.CitizenshipEnum import CitizenshipEnum


@ dataclass
class User:
    _id: int
    _full_name: str
    _citizenship: str #Гражданство
    _cars: List[Car] = field(default_factory=list)
    _birth_date: Optional[datetime] = None
    _owns_car: Optional[bool] = None #Наличие машины
    _departament: Optional[Departament] = None #Отдел сотрудника
    _workstation: Optional[Workstation] = None
    _role: Optional[Role] = None
    _position: Optional[Position] = None
    _probation_start: Optional[datetime] = None # дата начала испытательного срока
    _token: Optional[Token] = None

    @property
    def id(self) -> int:
        return self._id

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, full_name: str):
        self._full_name = full_name

    @property
    def birth_date(self)-> Optional[datetime]:
        return self._birth_date

    @birth_date.setter
    def birth_date(self, birth_date: datetime):
        if not isinstance(birth_date, datetime):
            raise TypeError ("Необходимо указать дату")
        self._birth_date = birth_date

    @property
    def citizenship(self) -> str:
        return self._citizenship

    @citizenship.setter
    def citizenship(self, citizenship: CitizenshipEnum):
         self._citizenship = citizenship.name

    @property
    def position(self) -> Optional[Position]:
        return self._position

    @position.setter
    def position(self, position: Position):
        self._position = position

    def add_car(self, car: Car):
        self._cars.append(car)

    def remove_car(self, id_car: int):
        for car in self._cars:
            if car.id == id_car:
                self._cars.remove(car)
                return
        raise ValueError (f"Автомобиль с ID {id_car} не найден")

    @property
    def cars(self) -> List[Car]:
        return self._cars

    @property
    def departament(self) -> Departament:
        return self._departament

    @departament.setter
    def departament(self, departament: Departament):
        self._departament = departament

    @property
    def workstation(self) -> Workstation:
        return self._workstation

    @workstation.setter
    def workstation(self, workstation: Workstation):
        self._workstation = workstation

    @property
    def role(self) -> Role:
        return self._role if self._role else "Не задана"

    @role.setter
    def role(self, role: Role):
        self._role = role

    @property
    def token(self) -> Optional[Token]:
        return self._token

    @token.setter
    def token(self, token: Token):
        self._token = token

    def is_on_probation(self) -> bool:
        if not self._probation_start:
            return False
        return (datetime.now()-self._probation_start).days < 90






