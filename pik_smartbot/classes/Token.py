from datetime import datetime, timezone, timedelta
import uuid
from dataclasses import dataclass, field
from typing import List, Optional, Type

from pik_smartbot.enums.PermissionsEnum import PermissionsEnum


@dataclass
class Token:
    _token: str = field(default_factory=lambda: str(uuid.uuid4()))
    _created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    _permissions: List[PermissionsEnum] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "token": self._token,
            "created_at": self._created_at.isoformat(),
            "permissions": [p.name for p in self._permissions]  # enum -> str
        }

    @classmethod
    def from_dict(cls, data: dict, permission_enum: Optional[Type[PermissionsEnum]] = None) -> "Token":
        if not isinstance(data.get("token"), str):
            raise ValueError("Invalid token string")

        try:
            created_at = datetime.fromisoformat(data["created_at"])
        except Exception as e:
            raise ValueError("Invalid datetime format") from e

        permissions = data.get("permissions", [])
        if not isinstance(permissions, list):
            raise ValueError("Permissions must be a list")

        if permission_enum:
            try:
                permissions = [permission_enum[p] for p in permissions]  # str -> enum
            except KeyError as e:
                raise ValueError(f"Unknown permission: {e.args[0]}")
        else:
            # если enum не передан — храним строки (не рекомендую)
            permissions = permissions

        return cls(
            _token=data["token"],
            _created_at=created_at,
            _permissions=permissions
        )

    @property
    def token(self) -> str:
        return self._token

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self._created_at + timedelta(hours=12)

    def update(self) -> None:
        self._token = str(uuid.uuid4())
        self._created_at = datetime.now(timezone.utc)

    def add_permission(self, permission: PermissionsEnum) -> bool:
        if permission not in self._permissions:
            self._permissions.append(permission)
            return True
        return False

    def remove_permission(self, permission: PermissionsEnum) -> bool:
        if permission in self._permissions:
            self._permissions.remove(permission)
            return True
        return False

    def check_permission(self, permission: PermissionsEnum) -> bool:
        return permission in self._permissions

    @property
    def permissions(self) -> List[PermissionsEnum]:
        return self._permissions.copy()  # defensive copy
