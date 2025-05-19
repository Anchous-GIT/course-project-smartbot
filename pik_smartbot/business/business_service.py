from dataclasses import dataclass
from datetime import datetime


from enums.CitizenshipEnum import CitizenshipEnum
from enums.RequestEnum import RequestEnum
from services.AccessControlService import AccessControlService
from services.DepartamentService import DepartamentService
from services.RequestService import RequestService
from services.UserService import UserService


@dataclass
class BusinessService:
    _user_svc: UserService
    _request_svc: RequestService
    _department_svc: DepartamentService
    _acs_svc: AccessControlService

    """Работа с пользователями----------------------------------------------------------------------------------------------"""

    def register_user(self, user_id: int, telegram_id: int, full_name: str,birth_date: datetime, citizenship: CitizenshipEnum):
        user = self._user_svc.create_user(user_id, telegram_id, full_name,birth_date, citizenship)
        return user

    def remove_user(self, user_id: int):
        user = self._user_svc.get_user_by_id(user_id)
        self._user_svc.remove_user(user)

    def rename_user(self, user_id: int, full_name: str):
        user = self._user_svc.get_user_by_id(user_id)
        user = self._user_svc.rename(user, full_name)
        return user


    def assign_user_to_department (self, id_departament: int, id_user: int, name: str):
        user = self._user_svc.get_user_by_id(id_user)
        departament = self._department_svc.get_departament_by_id(id_departament)
        if departament is None:
            departament = self._department_svc.create_departament(id_departament, name)
        user.department = departament
        self._user_svc.update_user(user)


    """Работа с заявками------------------------------------------------------------------------------------------------"""
    def create_request(self, id_request: int, user_id:int, request_type: RequestEnum):
        user = self._user_svc.get_user_by_id(user_id)
        request = self._request_svc.create_request(id_request, user, request_type)
        return request




