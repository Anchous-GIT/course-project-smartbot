from enum import Enum


class RoleEnum(Enum):
    DIRECTOR = "Директор"
    HEAD_OF_DEPARTMENT = "Начальник отдела"
    STUDENT = "Студент"
    ASSISTANT_CHIEF = "Помощник начальника отдела"
    PROBATION = "Сотрудник на испытательном сроке"
    PUBLIC_RELATIONS = "Сотрудник, отвечающий за связь с общественностью"
    OTHER = "Другое"