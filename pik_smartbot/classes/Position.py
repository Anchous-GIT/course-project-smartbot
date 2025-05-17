from dataclasses import dataclass
from pik_smartbot.enums.PositionEnum import PositionEnum


@dataclass
class Position:
    _id: int
    _name: str
    _requires_approval: bool #Подтвержденная или нет

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, position: PositionEnum):
        self._name = position.name

    @property
    def requires_approval(self) -> bool:
        return self._requires_approval

    @requires_approval.setter
    def requires_approval(self, value: bool):
        self._requires_approval = value



