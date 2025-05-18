import logging
from dataclasses import dataclass, field
from typing import Tuple

from pik_smartbot.classes.Request import Request
from pik_smartbot.classes.User import User
from pik_smartbot.enums.RequestEnum import RequestEnum, RequestStatusEnum

"""Исправить список заявок на БД
Добавить логирование ошибок
Добавить обновление бд, после изменения/создания заявки"""

@dataclass
class RequestService:
    _request_list: list[Request] = field(default_factory=list)

    def create_request(self, id_request: int, user: User, type: RequestEnum) -> Request:
        if not isinstance(id_request, int) or id_request < 0:
            raise ValueError ("Некорректный ID.")
        if id_request in [request.id for request in self._request_list]:
            raise ValueError (f"Заявка с ID {id_request} уже существует.")
        if not isinstance(user, User):
            raise ValueError("user не принадлежит классу User")
        if not isinstance(type, RequestEnum):
            raise ValueError("Тип заявки не принадлежит классу RequestEnum")
        request = Request(_id=id_request, _user=user, _type=type, _status=RequestStatusEnum.PENDING)
        self._request_list.append(request)
        logging.info(f"Created request '{type.name}' with ID {id_request}")
        return request

    def get_request_by_id(self, id_request: int) -> Request:
        if not isinstance(id_request, int) or id_request < 0:
            raise ValueError("Некорректный ID")
        for request in self._request_list:
            if request.id == id_request:
                return request
        raise ValueError("Заявка не найдена")

    @property
    def request_list(self) -> list[Request]:
        return self._request_list

    def state_by_id(self, id_request: int) -> Tuple[int, RequestEnum, RequestStatusEnum, User]:
        request = self.get_request_by_id(id_request)
        return request.id, request.type, request.status, request.user

    def update_status_request(self, id_request: int, status: RequestStatusEnum) -> None:
        if not isinstance(id_request, int) or id_request < 0:
            raise ValueError("Некорректный ID")
        if not isinstance(status, RequestStatusEnum):
            raise ValueError("Тип статуса не принадлежит классу RequestStatusEnum")
        request = self.get_request_by_id(id_request)
        request.status = status
        logging.info(f"Updated status of request '{request.type.name}' with ID {id_request} to '{status.name}'")

