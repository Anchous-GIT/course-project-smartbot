from dataclasses import dataclass, field

from pik_smartbot.enums import RoleEnum
from pik_smartbot.enums.PermissionsEnum import PermissionsEnum


@dataclass
class Role:
    _id: int
    _name: RoleEnum
    _permissions: set[PermissionsEnum] = field(default_factory=set)

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, role: RoleEnum):
        self._name = role.name

    @property
    def permissions(self) -> set[PermissionsEnum]:
        return self._permissions

    def add_permission(self, permission: PermissionsEnum):
        if permission not in self._permissions:
            self._permissions.add(permission)

    def remove_permission(self, permission: PermissionsEnum):
        if permission in self._permissions:
            self._permissions.discard(permission)


