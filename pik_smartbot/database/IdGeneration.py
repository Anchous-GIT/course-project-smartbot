from dataclasses import dataclass, field
from itertools import count
from typing import Iterator

@dataclass
class IdGeneration:
    _users_id: Iterator[int] = field(default_factory=lambda: count(1))
    _requests_id: Iterator[int] = field(default_factory=lambda: count(1))
    _roles_id: Iterator[int] = field(default_factory=lambda: count(1))
    _positions_id: Iterator[int] = field(default_factory=lambda: count(1))
    _departaments_id: Iterator[int] = field(default_factory=lambda: count(1))
    _workstations_id: Iterator[int] = field(default_factory=lambda: count(1))

    def get_next_user_id(self) -> int:
        return next(self._users_id)

    def get_next_request_id(self) -> int:
        return next(self._requests_id)

    def get_next_role_id(self) -> int:
        return next(self._roles_id)

    def get_next_position_id(self) -> int:
        return next(self._positions_id)

    def get_next_departament_id(self) -> int:
        return next(self._departaments_id)

    def get_next_workstation_id(self) -> int:
        return next(self._workstations_id)

    def set_start_ids(
            self,
            user_id: int,
            request_id: int,
            role_id: int,
            position_id: int,
            departament_id: int,
            workstation_id: int
    ) -> None:
        self._users_id = count(user_id + 1)
        self._requests_id = count(request_id + 1)
        self._roles_id = count(role_id + 1)
        self._positions_id = count(position_id + 1)
        self._departaments_id = count(departament_id + 1)
        self._workstations_id = count(workstation_id + 1)

id_gen = IdGeneration()