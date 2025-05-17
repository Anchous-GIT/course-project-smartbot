from enum import Enum, auto


class PermissionsEnum(Enum):
    FULl_ACCESS = auto()
    VIEW_USERS =auto()
    EDIT_USERS = auto()

permission_descriptions = {
        PermissionsEnum.FULl_ACCESS: "Полный доступ ко всем данным (не рекомендуется)",
    PermissionsEnum.EDIT_USERS: "Редактирование",
    PermissionsEnum.VIEW_USERS: "Просмотр"
}