from dataclasses import dataclass
from classes.User import User
from database.IdGeneration import id_gen
from enums.RequestEnum import RequestEnum, RequestStatusEnum


@dataclass
class  Request:
    _id_request: int
    _user: User
    _type: RequestEnum
    _status: RequestStatusEnum
    _value_request: str
    _responsible: User = None

    def to_dict(self) -> dict:
        return {
            "id_request": self._id_request,
            "user": self._user.id,  # или user.to_dict() — если есть
            "type": self._type.name,
            "status": self._status.name,
            "value_request": self._value_request,
            "responsible": self._responsible.id if self._responsible else None
        }

    @classmethod
    def from_dict(cls, data: dict):
        id_request = data.get("id_request")
        if not isinstance(id_request, int) or id_request < 0:
            raise ValueError("Некорректный ID заявки")
        user_data = data.get("user")

        from database.Database import db
        if not isinstance(user_data, int):
            raise ValueError("Некорректные данные пользователя")
        user = db.get_user_by_id(user_data)

        request_type = data.get("type")
        if not isinstance(request_type, str) or request_type not in RequestEnum.__members__:
            raise ValueError("Некорректный тип заявки")

        status_name = data.get("status")
        if not isinstance(status_name, str) or status_name not in RequestStatusEnum.__members__:
            raise ValueError("Некорректный статус заявки")

        value_request = data.get("value_request")
        if not isinstance(value_request, str):
            raise ValueError("Некорректный текст заявки")

        responsible_data = data.get("responsible")
        if responsible_data is not None:
            if not isinstance(responsible_data, dict):
                raise ValueError("Некорректные данные ответственного")
            responsible = User.from_dict(responsible_data)
        else:
            responsible = None

        return cls(
            _id_request=id_request,
            _user=user,
            _type=RequestEnum.__members__[request_type],  # ← Enum
            _status=RequestStatusEnum.__members__[status_name],  # ← Enum
            _value_request=value_request,
            _responsible=responsible
        )

    @classmethod
    def create(cls, user: User, request_type: RequestEnum, value_request:str):
        id_request = id_gen.get_next_request_id()
        if not isinstance(id_request, int) or id_request < 0:
            raise ValueError("Некорректный ID.")
        if not isinstance(user, User):
            raise ValueError("user не принадлежит классу User")
        if not isinstance(request_type, RequestEnum):
            raise ValueError("Тип заявки не принадлежит классу RequestEnum")
        if not isinstance(value_request, str):
            raise ValueError("Текст запроса должен быть строкой")

        status = RequestStatusEnum.PENDING
        return cls(_id_request=id_request, _user=user, _type=request_type, _status=status, _value_request=value_request)

    @property
    def id(self) -> int:
        return self._id_request

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
        if not isinstance(status, RequestStatusEnum):
            raise TypeError("Статус должен быть экземпляром RequestStatusEnum")
        self._status = status

    @property
    def value_request(self) -> str:
        return self._value_request

    @property
    def responsible(self) -> User:
        if self._responsible is not None:
            return self._responsible
        else:
            raise ValueError (f"Нет закрепленного ответственного")

    @responsible.setter
    def responsible(self, user: User):
        self._responsible = user
