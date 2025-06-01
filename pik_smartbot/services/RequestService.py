import logging
from dataclasses import dataclass
from typing import Tuple

from database.Database import db
from pik_smartbot.classes.Request import Request
from pik_smartbot.classes.User import User
from pik_smartbot.enums.RequestEnum import RequestEnum, RequestStatusEnum

"""Исправить список заявок на БД
Добавить логирование ошибок
Добавить обновление бд, после изменения/создания заявки"""

@dataclass
class RequestService:

    @staticmethod
    def request_verification(request: Request):
        if not isinstance(request, Request):
            raise ValueError("Request is not an instance of Request class")
        if not request.id:
            raise ValueError("Request ID is required")
        if not request.type:
            raise ValueError("Request type is required")
        if not request.user:
            raise ValueError("Request user is required")

    @staticmethod
    def update_request(request: Request) -> Request:
        RequestService.request_verification(request)
        logging.info(f"Updated request '{request.type.name}' with ID {request.id}")
        return request

    def create_request(self, user: User, type_enum: RequestEnum, value_request:str) -> Request:
        request = Request.create(user, type_enum, value_request)
        db.add_request(request)
        logging.info(f"Created request '{type_enum.name}' with ID {request.id}")
        self.update_request(request)
        return request

    def state_by_id(self, id_request: int) -> Tuple[int, RequestEnum, RequestStatusEnum, User]:
        request = db.get_request_by_id(id_request)
        return request.id, request.type, request.status, request.user

    def update_status_request(self, id_request: int, status: RequestStatusEnum) -> None:
        if not isinstance(id_request, int) or id_request < 0:
            raise ValueError("Некорректный ID")
        if not isinstance(status, RequestStatusEnum):
            raise ValueError("Тип статуса не принадлежит классу RequestStatusEnum")
        request = db.get_request_by_id(id_request)
        request.status = status
        logging.info(f"Updated status of request '{request.type.name}' with ID {id_request} to '{status.name}'")

