from dataclasses import dataclass, field
from typing import List
from pik_smartbot.classes.Workstation import Workstation

#Даем возможность менять имя отдела, добавлять/удалять рабочие места
@ dataclass
class Departament:
    _id_departament: int
    _name_departament: str

    _workstations: List["Workstation"] = field(default_factory=list)

    @property
    def id_departament(self)-> int:
        return self._id_departament

    @property
    def name_departament(self) -> str:
        return self._name_departament

    @name_departament.setter
    def name_departament(self,name_departament:str):
        self._name_departament = name_departament


    @property
    def workstations(self)-> list[Workstation]:
        return self._workstations

    def add_workstation(self, workstation: Workstation):
        self._workstations.append(workstation)

    def remove_workstation(self, id_workstation: int) -> None:
        for workstation in self._workstations:
            if workstation.id == id_workstation:
                self._workstations.remove(workstation)
                return
        raise ValueError(f"Место с ID {id_workstation} не найдено.")

