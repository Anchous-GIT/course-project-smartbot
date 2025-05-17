from dataclasses import dataclass
from enum import Enum


@dataclass
class RequestEnum(Enum):
    USER_UPDATE = "Изменение данных пользователя"
    ACCESS_REQUEST = "Запрос доступа"
    FINANCE_REQUEST = "Заявка в бухгалтерию"
    HR_REQUEST = "Заявка в отдел кадров"

class RequestStatusEnum(Enum):
    IN_PROGRESS = "В процессе"
    COMPLETED = "Завершено"
    PENDING = "Ожидает обработки"