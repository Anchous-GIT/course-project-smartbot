from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from pik_smartbot.classes.Role import Role
from pik_smartbot.classes.Position import Position
from pik_smartbot.classes.Car import Car
from pik_smartbot.classes.Token import Token
from pik_smartbot.classes.Departament import Departament
from pik_smartbot.classes.Workstation import Workstation
from pik_smartbot.enums.CitizenshipEnum import CitizenshipEnum

"""Добавить проверку типов, обязательности, форматов"""

@ dataclass
class User:
    _id: int
    _telegram_id: int
    _full_name: str
    _citizenship: CitizenshipEnum #Гражданство
    _cars: List[Car] = field(default_factory=list)
    _birth_date: Optional[datetime] = None
    _owns_car: Optional[bool] = None #Наличие машины
    _departament: Optional[Departament] = None #Отдел сотрудника
    _workstation: Optional[Workstation] = None
    _role: Optional[Role] = None
    _position: Optional[Position] = None
    _probation_start: Optional[datetime] = None # дата начала испытательного срока
    _token: Optional[Token] = None


    def __post_init__(self):
        if not isinstance(self._id, int) or self._id < 0:
            raise ValueError ("Некорректный ID пользователя")
        if not isinstance(self._telegram_id, int) or self._telegram_id < 0:
            raise ValueError ("Некорректный ID телеграмма")
        if not isinstance(self._full_name, str) or self._full_name.strip() == "":
            raise ValueError("Некорректное ФИО пользователя")
        if not isinstance(self._citizenship, CitizenshipEnum):
            raise ValueError("Гражданство пользователя не является объектом класса CitizenshipEnum")
        if self._owns_car is None:
            self._owns_car = False
        if not self._probation_start:
            self._probation_start = datetime.now()

    @property
    def id(self) -> int:
        return self._id

    @property
    def telegram_id(self) -> int:
        return self._telegram_id

    @telegram_id.setter
    def telegram_id(self, telegram_id: int):
        if isinstance(telegram_id, int) or telegram_id < 0:
            raise ValueError("Некорректный ID telegram")
        self._telegram_id = telegram_id

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, full_name: str):
        if not isinstance(full_name, str) or not full_name.strip():
            raise ValueError("Некорректное имя пользователя")
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
    def citizenship(self) -> CitizenshipEnum:
        return self._citizenship

    @citizenship.setter
    def citizenship(self, citizenship: CitizenshipEnum):
         if citizenship not in CitizenshipEnum:
             raise ValueError("Гражданство пользователя не является объектом класса CitizenshipEnum")
         self._citizenship = citizenship

    @property
    def position(self) -> Optional[Position]:
        return self._position

    @position.setter
    def position(self, position: Position):
        if not isinstance(position, Position):
            raise ValueError("Позиция пользователя не является объектом класса Position")
        self._position = position

    def add_car(self, car: Car):
        if not isinstance(car, Car):
            raise ValueError("Машина пользователя не является объектом класса Car")
        self._cars.append(car)

    def remove_car(self, id_car: int):
        if not isinstance(id_car,int) or id_car < 0:
            raise ValueError("Некорректный ID")
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
        if not isinstance(workstation, Workstation):
            raise ValueError("Место пользователя не является объектом класса Workstation")
        self._workstation = workstation

    @property
    def role(self) -> Optional[Role]:
        return self._role if self._role else "Не задана"

    @role.setter
    def role(self, role: Role):
        if not isinstance(role, Role):
            raise ValueError("Роль пользователя не является объектом класса Role")
        self._role = role

    @property
    def token(self) -> Optional[Token]:
        return self._token

    @token.setter
    def token(self, token: Token):
        if not isinstance(token, Token):
            raise ValueError("Токен пользователя не является объектом класса Token")
        self._token = token

    def is_on_probation(self) -> bool:
        if not self._probation_start:
            return False
        return (datetime.now()-self._probation_start).days < 90






