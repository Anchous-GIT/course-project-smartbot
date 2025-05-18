# DepartamentService

**Описание:**  
Сервис управления отделами (департаментами) компании. Отвечает за создание отделов, добавление и удаление пользователей и рабочих мест в отделах, а также получение списка рабочих мест отдела.

**Поля:**
- `_departaments: list[Departament]` — список всех департаментов, управляемых сервисом

**Свойства:**
- `departaments` — чтение списка всех департаментов

**Методы:**
- `new_departament(id_departament: int, name: str) -> Departament` — создание нового департамента с уникальным ID и именем
- `add_user_to_departament(departament: Departament, user: User) -> None` — добавить пользователя в указанный департамент, с последующим обновлением данных пользователя через `UserService`
- `remove_user_from_departament(user: User) -> None` — удалить пользователя из департамента, обнуляя связь и обновляя данные через `UserService`
- `add_workstation_to_departament(departament: Departament, workstation: Workstation) -> Departament` — добавить рабочее место в департамент
- `remove_workstation_from_departament(departament: Departament, workstation: Workstation) -> Departament` — удалить рабочее место из департамента по объекту рабочего места
- `remove_workstation_from_departament_id(departament: Departament, id_departament: int) -> Departament` — удалить рабочее место из департамента по ID рабочего места
- `list_workstations_in_departament(departament: Departament) -> list[Workstation]` — получить список всех рабочих мест в департаменте
- `get_departament_by_id(id_departament: int) -> Optional[Departament]` — получить департамент по ID или вернуть None, если не найден
    
**Связи:**
- Связь с классом [[DepartamentClass]] (хранит и управляет объектами департаментов)
- Связь с классом [[UserClass]] (управляет добавлением/удалением пользователей в департаменты)
- Связь с классом [[WorkstationClass]] (управляет рабочими местами в департаментах)
- Связь с сервисом [[UserServise]] (обновляет данные пользователей при изменениях)