from dataclasses import dataclass

from pik_smartbot.classes import User
from pik_smartbot.enums.RequestEnum import RequestStatusEnum, RequestEnum


@dataclass
class  Request:
    _id: int
    _user: User
    _type: RequestEnum
    _status: RequestStatusEnum
    _responsible: User = None

    @property
    def id(self) -> int:
        return self._id

    @property
    def user(self) -> User:
        return self._user

    @property
    def type(self) -> RequestEnum:
        return self._type

    @property
    def status(self) -> RequestStatusEnum:
        return self._status

    @status.setter
    def status(self, status: RequestStatusEnum):
        self._status = status

    @property
    def responsible(self) -> User:
        if self._responsible is not None:
            return self._responsible
        else:
            raise ValueError (f"Нет закрепленного ответственного")


    @responsible.setter
    def responsible(self, user: User):
        self._responsible = user
