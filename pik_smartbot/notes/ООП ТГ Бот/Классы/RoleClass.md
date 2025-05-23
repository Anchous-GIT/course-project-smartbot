# Role
**Описание:**  
Класс, представляющий роль пользователя в системе. Содержит идентификатор, название роли и набор разрешений, которые определяют права пользователя с данной ролью.

**Поля:**
- `_id: int` — уникальный идентификатор роли
- `_name: RoleEnum` — название роли (используется перечисление RoleEnum)
- `_permissions: set[PermissionsEnum]` — множество разрешений, связанных с ролью
    
**Свойства:**
- `id` — чтение уникального идентификатора роли
- `name` — чтение и запись названия роли; при записи принимает значение из `RoleEnum`, сохраняет строковое имя роли
- `permissions` — чтение множества разрешений роли

**Методы:**
- `add_permission(permission: PermissionsEnum) -> None` — добавляет разрешение в множество, если его там ещё нет
- `remove_permission(permission: PermissionsEnum) -> None` — удаляет разрешение из множества, если оно там присутствует
    
**Связи:**
- Использует перечисления [[Role]] и [[Permissions]] для названия роли и разрешений соответственно