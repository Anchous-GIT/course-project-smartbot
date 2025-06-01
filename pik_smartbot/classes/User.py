from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from classes.Car import Car
from classes.Departament import Departament
from classes.Position import Position
from classes.Role import Role
from classes.Token import Token
from classes.Workstation import Workstation
from enums.CitizenshipEnum import CitizenshipEnum

"""Добавить проверку типов, обязательности, форматов"""

@ dataclass
class User:
    _id: int
    _telegram_id: int
    _full_name: str
    _citizenship: CitizenshipEnum #Гражданство
    _birth_date: datetime
    _cars: List[Car] = field(default_factory=list)
    _owns_car: Optional[bool] = None #Наличие машины
    _departament: Optional[Departament] = None #Отдел сотрудника
    _workstation: Optional[Workstation] = None
    _role: Optional[Role] = None
    _position: Optional[Position] = None
    _probation_start: Optional[datetime] = None # дата начала испытательного срока
    _token: Optional[Token] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "full_name": self.full_name,
            "citizenship": self.citizenship.value,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "cars": [car.to_dict() for car in self.cars],
            "owns_car": self._owns_car,
            "departament": self.departament.name if self.departament else None,
            "workstation": self.workstation.number if self.workstation else None,
            "role": self.role.to_dict() if self.role else None,
            "position": self.position.to_dict() if self.position else None,
            "probation_start": self._probation_start.isoformat() if self._probation_start else None,
            "token": self.token.to_dict() if self.token else None,
        }

    @classmethod
    def from_dict(cls, data: dict):
        # Проверки на обязательные поля
        if not isinstance(data.get("id"), int) or data["id"] < 0:
            raise ValueError("Invalid user ID")
        if not isinstance(data.get("telegram_id"), int) or data["telegram_id"] < 0:
            raise ValueError("Invalid telegram ID")
        full_name = data.get("full_name")
        if not isinstance(full_name, str) or not full_name.strip():
            raise ValueError("Invalid full name")
        birth_date_str = data.get("birth_date")
        if not isinstance(birth_date_str, str):
            raise ValueError("Invalid birth date format")
        # Convert birth_date string to datetime
        try:
            birth_date = datetime.fromisoformat(birth_date_str)
        except Exception as e:
            raise ValueError(f"Invalid birth_date format: {e}")

        citizenship_str = data.get("citizenship")
        try:
            citizenship = CitizenshipEnum(citizenship_str)
        except KeyError:
            raise ValueError(f"Invalid citizenship value: {citizenship_str}")

        # Convert cars list of dicts to list of Car objects
        cars_data = data.get("cars", [])
        if not isinstance(cars_data, list):
            raise ValueError("Invalid cars list")
        cars = [Car.from_dict(car_dict) for car_dict in cars_data]

        # Optional fields
        owns_car = data.get("owns_car")
        if owns_car is not None and not isinstance(owns_car, bool):
            raise ValueError("Invalid owns_car flag")

        # For departament, workstation, role, position, token - assume they have from_dict or similar
        departament_data = data.get("departament")
        departament = Departament.from_dict(departament_data) if departament_data else None

        workstation_data = data.get("workstation")
        workstation = Workstation.from_dict(workstation_data) if workstation_data else None

        role_data = data.get("role")
        role = Role.from_dict(role_data) if role_data else None

        position_data = data.get("position")
        position = Position.from_dict(position_data) if position_data else None

        probation_start_str = data.get("probation_start")
        probation_start = None
        if probation_start_str:
            try:
                probation_start = datetime.fromisoformat(probation_start_str)
            except Exception as e:
                raise ValueError(f"Invalid probation_start format: {e}")

        token_data = data.get("token")
        token = Token.from_dict(token_data) if token_data else None

        return cls(
            _id=data["id"],
            _telegram_id=data["telegram_id"],
            _full_name=full_name,
            _citizenship=citizenship,
            _birth_date=birth_date,
            _cars=cars,
            _owns_car=owns_car,
            _departament=departament,
            _workstation=workstation,
            _role=role,
            _position=position,
            _probation_start=probation_start,
            _token=token,
        )

    @classmethod
    def create(cls, id_user: int, telegram_id: int, full_name: str, birth_date: datetime, citizenship: CitizenshipEnum, owns_car: bool = False,
               probation_start=None):
        if not (isinstance(id_user, int) and id_user >= 0):
            raise ValueError("Invalid user ID")
        if not (isinstance(telegram_id, int) and telegram_id >= 0):
            raise ValueError("Invalid telegram ID")
        if not (isinstance(full_name, str) and full_name.strip()):
            raise ValueError("Invalid full name")
        if not (isinstance(birth_date, datetime) and birth_date.year >= 1920):
            raise ValueError("Invalid birth date")
 #       if not isinstance(citizenship, CitizenshipEnum):
  #          raise ValueError(f"Invalid citizenship, {citizenship}")
        return cls(_id=id_user, _telegram_id=telegram_id, _full_name=full_name, _citizenship=citizenship,_birth_date=birth_date, _owns_car=owns_car, _probation_start=probation_start)

    @property
    def id(self) -> int:
        return self._id

    @property
    def telegram_id(self) -> int:
        return self._telegram_id

    @telegram_id.setter
    def telegram_id(self, telegram_id: int):
        if not isinstance(telegram_id, int) or telegram_id < 0:
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
            raise ValueError("Должность пользователя не является объектом класса Position")
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
        if not isinstance(departament, Departament):
            raise ValueError("Передаваемый отдел пользователя не является объектом класса Departament")
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
        return self._role

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








