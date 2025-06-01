from dataclasses import dataclass, field
from typing import List
from classes.Workstation import Workstation
from database.IdGeneration import id_gen


#Даем возможность менять имя отдела, добавлять/удалять рабочие места
@ dataclass
class Departament:
    _id: int
    _name: str
    _workstations: List["Workstation"] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "workstations": [ws.to_dict() for ws in self._workstations]
        }

    @classmethod
    def from_dict(cls, data: dict):
        id_departament = data.get("id")
        if not isinstance(id_departament, int) or id_departament < 0:
            raise ValueError("Invalid department ID")

        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid department name")

        workstations_data = data.get("workstations", [])
        if not isinstance(workstations_data, list):
            raise ValueError("Workstations should be a list")

        workstations = []
        for ws_data in workstations_data:
            if not isinstance(ws_data, dict):
                raise ValueError("Invalid workstation data")
            workstation = Workstation.from_dict(ws_data)  # <-- важный момент
            workstations.append(workstation)

        return cls(id_departament, name, workstations)

    @classmethod
    def create(cls, name: str, workstations: list["Workstation"] = None):
        id_departament = id_gen.get_next_departament_id()

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid department name")

        # Если workstations — None, заменим на пустой список
        if workstations is None:
            workstations = []
        elif not isinstance(workstations, list) or not all(isinstance(ws, Workstation) for ws in workstations):
            raise ValueError("Invalid list of workstations")

        return cls(_id=id_departament, _name=name, _workstations=workstations)

    @property
    def id(self)-> int:
        return self._id

    @property
    def name(self)-> str:
        return self._name

    @name.setter
    def name(self,name_departament:str) -> None:
        if not isinstance(name_departament,str) or not name_departament.strip():
            raise TypeError("Необходимо ввести строковое значение")
        self._name = name_departament

    @property
    def workstations(self)-> list[Workstation]:
        return self._workstations

    def add_workstation(self, workstation: Workstation) -> None:
        if not isinstance(workstation, Workstation):
            raise TypeError("Должен быть передан объект класса Workstation")
        self._workstations.append(workstation)

    def _remove_workstation(self, predicate) -> None:
        for ws in self._workstations:
            if predicate(ws):
                self._workstations.remove(ws)
                return
        raise ValueError("Workstation not found.")

    def remove_workstation_by_id(self, id_workstation: int) -> None:
        if not isinstance(id_workstation, int) or id_workstation < 0:
            raise ValueError("Некорректный ID места")
        self._remove_workstation(lambda ws: ws.id == id_workstation)

    def remove_workstation(self, workstation: Workstation) -> None:
        if not isinstance(workstation, Workstation):
            raise TypeError("Должен быть объект Workstation")
        self._remove_workstation(lambda ws: ws == workstation)