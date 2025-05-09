from dataclasses import dataclass
from datetime import datetime

from pik_smartbot.enums.Citizenship import Citizenship


@dataclass
class UserRegistrationDTO:
    id:int
    full_name: str
    birth_date: datetime
    citizenship: Citizenship

