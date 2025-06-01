from typing import Tuple
from datetime import datetime

from database.Database import db
from enums.CitizenshipEnum import CitizenshipEnum
from enums.PositionEnum import PositionEnum
from enums.RoleEnum import RoleEnum
from services.DepartamentService import DepartamentService


def validate_full_name(name: str) -> Tuple[bool, str]:
    parts = name.strip().split()
    if len(parts) < 2:
        return False, "Полное имя должно содержать не менее двух слов."
    if any(char.isdigit() for char in name):
        return False, "Полное имя не может содержать цифры."
    return True, ""

def validate_birth_date(date_str: str) -> Tuple[bool, str]:
    try:
        dob = datetime.strptime(date_str, "%d.%m.%Y")
        if dob >= datetime.now():
            return False, "Дата рождения не может быть в будущем."
        if (datetime.now() - dob).days < 18 * 365:
            return False, "Вам должно быть не менее 18 лет."
        return True, ""
    except ValueError:
        return False, "Неверный формат даты. Используйте ДД.ММ.ГГГГ"

def validate_citizenship(value: str) -> Tuple[bool, str]:
    try:
        CitizenshipEnum(value.upper())
        return True, ""
    except KeyError:
        return False, f"Недействительное гражданство. Выберите одно из: {', '.join([e.name for e in CitizenshipEnum])}"

def validate_department(department: str) -> Tuple[bool, str]:
    valid_departments = [d.name for d in db.get_departaments_list.departaments]
    if department not in valid_departments:
        return False, f"Отдел '{department}' не найден. Выберите один из: {', '.join(valid_departments)}"
    return True, ""

def validate_workstation(workstation_str: str,departament_name: str, departament_service: DepartamentService) -> Tuple[bool, str]:
    # Проверка, что введённое значение — число
    if not workstation_str.isdigit():
        return False, "Номер рабочего места должен быть числом."

    workstation_number = int(workstation_str)

    # Поиск отдела
    departament = db.get_departament_by_name(departament_name)
    if not departament:
        return False, f"Отдел '{departament_name}' не найден."

    # Получаем рабочие места в отделе
    workstations = departament_service.list_workstations_in_departament(departament)
    valid_numbers = [ws.number for ws in workstations]  # предполагаем, что у Workstation есть атрибут .number

    # Проверка наличия номера
    if workstation_number not in valid_numbers:
        return False, f"Рабочее место '{workstation_number}' не найдено. Доступные номера: {', '.join(map(str, valid_numbers))}"

    return True, ""

def validate_position(position: str) -> Tuple[bool, PositionEnum | str]:
    normalized_input = position.strip().lower()

    for enum_member in PositionEnum:
        if enum_member.value.lower() == normalized_input:
            return True, enum_member

    valid_values = ', '.join([e.value for e in PositionEnum])
    return False, f"❌ Недействительная должность. Выберите одну из: {valid_values}"

def validate_role(role: str) -> Tuple[bool, RoleEnum | str]:
    normalized_input = role.strip().lower()

    for enum_member in RoleEnum:
        if enum_member.value.lower() == normalized_input:
            return True, enum_member

    valid_values = ', '.join([e.value for e in RoleEnum])
    return False, f"❌ Недействительная роль. Выберите одну из: {valid_values}"

