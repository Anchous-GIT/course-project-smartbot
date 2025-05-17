from datetime import datetime, timezone, timedelta
import uuid
from dataclasses import dataclass, field
from typing import List

from pik_smartbot.enums.PermissionsEnum import PermissionsEnum


@dataclass
class Token:
    _token: str = field(default_factory=lambda: str(uuid.uuid4()))
    _created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    _permissions: List[str] = field(default_factory=list)

    @property
    def token(self) -> str:
        return self._token

    @property
    def created_at(self) -> datetime:
        return self._created_at

    # Check if token is expired (valid for 12 hours)
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self._created_at + timedelta(hours=12)

    # Generate new token and reset timestamp
    def update(self) -> None:
        self._token = str(uuid.uuid4())
        self._created_at = datetime.now(timezone.utc)

    # Add permission if not already present
    def add_permission(self, permission: PermissionsEnum) -> bool:
        if permission.name not in self._permissions:
            self._permissions.append(permission.name)
            return True
        return False

    # Remove permission if exists
    def remove_permission(self, permission: PermissionsEnum) -> bool:
        if permission.name in self._permissions:
            self._permissions.remove(permission.name)
            return True
        return False

    # Check if token has specific permission
    def check_permission(self, permission: PermissionsEnum) -> bool:
        return permission.name in self._permissions

    @property
    def permissions(self) -> List[str]:
        return self._permissions.copy()  # defensive copy
