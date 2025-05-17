from dataclasses import dataclass
from datetime import datetime

from pik_smartbot.classes.Departament import Departament
from pik_smartbot.enums.CitizenshipEnum import CitizenshipEnum


@dataclass
class UserRegistrationDTO:
    id:int
    full_name: str
    birth_date: datetime
    citizenship: CitizenshipEnum
    own_car: bool
    department: Departament




