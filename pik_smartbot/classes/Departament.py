from dataclasses import dataclass, field
from typing import List
from pik_smartbot.classes.Workstation import Workstation

#Даем возможность менять имя отдела, добавлять/удалять рабочие места
@ dataclass
class Departament:
    _id: int
    _name: str
    _workstations: List["Workstation"] = field(default_factory=List)

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

    def add_workstation(self, workstation: Workstation):
        if not isinstance(workstation, Workstation):
            raise TypeError("Должен быть передан объект класса Workstation")
        self._workstations.append(workstation)

    def remove_workstation_by_id(self, id_workstation: int) -> None:
        for workstation in self._workstations:
            if workstation.id == id_workstation:
                self._workstations.remove(workstation)
                return
        raise ValueError(f"Место с ID {id_workstation} не найдено.")

    def remove_workstation(self, workstation: Workstation) -> None:
        for workstations in self._workstations:
            if workstations == workstation:
                self._workstations.remove(workstation)
                return
        raise ValueError(f"Место с ID {workstation.id} не найдено.")

