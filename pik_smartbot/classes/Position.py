from dataclasses import dataclass

from database.IdGeneration import id_gen
from enums.PositionEnum import PositionEnum


@dataclass
class Position:
    _id: int
    _name: PositionEnum
    _requires_approval: bool

    # to_dict теперь отдаёт строковое значение enum
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name": self._name.value,  # enum.value, а не name
            "requires_approval": self._requires_approval
        }

    @classmethod
    def from_dict(cls, data: dict):
        id_position = data.get("id")
        if not isinstance(id_position, int) or id_position < 0:
            raise ValueError("Invalid position ID")
        name = data.get("name")
        try:
            position_enum = PositionEnum(name)
        except ValueError:
            raise ValueError("Invalid position name")
        requires_approval = data.get("requires_approval", False)
        if not isinstance(requires_approval, bool):
            raise ValueError("Invalid requires_approval value")
        return cls(_id=id_position, _name=position_enum, _requires_approval=requires_approval)

    @classmethod
    def create(cls,  name: PositionEnum, requires_approval: bool = False):
        id_position = id_gen.get_next_position_id()

        if not isinstance(id_position, int) or id_position < 0:
            raise ValueError("Invalid position ID")
        if not isinstance(name, PositionEnum):
            raise ValueError("Invalid position name")
        return cls(_id=id_position, _name=name, _requires_approval=requires_approval)

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> PositionEnum:
        return self._name

    @name.setter
    def name(self, position: PositionEnum):
        if not isinstance(position, PositionEnum):
            raise ValueError("Position must be a PositionEnum")
        self._name = position

    @property
    def requires_approval(self) -> bool:
        return self._requires_approval

    @requires_approval.setter
    def requires_approval(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("requires_approval must be bool")
        self._requires_approval = value

    @staticmethod
    def get_position_enum_by_name(name: str) -> PositionEnum | None:
        try:
            return PositionEnum(name)
        except ValueError:
            return None
