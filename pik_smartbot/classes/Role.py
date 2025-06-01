from dataclasses import dataclass, field

from database.IdGeneration import id_gen
from enums.RoleEnum import RoleEnum
from pik_smartbot.enums.PermissionsEnum import PermissionsEnum


@dataclass
class Role:
    _id_role: int
    _name: RoleEnum
    _permissions: set[PermissionsEnum] = field(default_factory=set)

    @classmethod
    def create(cls, name: RoleEnum, permissions: list[PermissionsEnum] = None):
        id_role = id_gen.get_next_role_id()
        if not (isinstance(id_role, int) and id_role >=0):
            raise ValueError("Invalid role ID")
        if not isinstance(name, RoleEnum):
            raise ValueError(f"Invalid role name")
        permissions = permissions or []
        return cls(_id_role=id_role, _name=name, _permissions=set(permissions))

    @classmethod
    def create_for_name_enum(cls, name: str, permissions: list[PermissionsEnum] = None):
        role_enum = cls.get_role_by_name(name)
        if role_enum is None:
            raise ValueError(f"Invalid role name {name}")
        return cls.create(role_enum, permissions)

    def to_dict(self) -> dict:
        return {
            "id_role": self._id_role,
            "name": self._name.name,  # или str(self._name)
            "permissions": [perm.name for perm in self._permissions],
        }

    @classmethod
    def from_dict(cls, data: dict):
        id_role = data.get("id_role")
        if not isinstance(id_role, int) or id_role < 0:
            raise ValueError("Invalid role ID")

        name = data.get("name")
        if not isinstance(name, str) or name not in RoleEnum.__members__:
            raise ValueError("Invalid role name")

        permissions = data.get("permissions", [])
        if not isinstance(permissions, list):
            raise ValueError("Invalid permissions list")

        # Преобразуем строки в PermissionsEnum
        permissions_set = set()
        for perm_str in permissions:
            if not isinstance(perm_str, str) or perm_str not in PermissionsEnum.__members__:
                raise ValueError(f"Invalid permission: {perm_str}")
            permissions_set.add(PermissionsEnum(perm_str))

        return cls(_id_role=id_role, _name=RoleEnum.__members__[name], _permissions=permissions_set)

    @property
    def id(self) -> int:
        return self._id_role

    @property
    def name(self) -> RoleEnum:
        return self._name

    @name.setter
    def name(self, role: RoleEnum):
        self._name = role

    #На всякий случай, чтобы список не мутировал
    @property
    def permissions(self) -> frozenset[PermissionsEnum]:
        return frozenset(self._permissions)

    def add_permission(self, permission: PermissionsEnum):
        if permission not in self._permissions:
            self._permissions.add(permission)

    def remove_permission(self, permission: PermissionsEnum):
        self._permissions.discard(permission)

    @staticmethod
    def get_role_by_name(name: str) -> RoleEnum | None:
        try:
            return RoleEnum.__members__[name]
        except KeyError:
            return None

