from dataclasses import dataclass

from database.IdGeneration import id_gen


@ dataclass
class Workstation:
    _id_workstation: int
    _number: int
    _content_workstation: str

    def to_dict(self) -> dict:
        return {
            "id_workstation": self._id_workstation,
            "number": self._number,
            "content_workstation": self._content_workstation,
        }

    @classmethod
    def from_dict(cls, data: dict):
        id_workstation = data.get("id_workstation")
        if not isinstance(id_workstation, int) or id_workstation < 0:
            raise ValueError("Некорректный ID места")

        number = data.get("number")
        if not isinstance(number, int) or number < 0:
            raise ValueError("Некорректный номер места пользователя")

        content = data.get("content_workstation")
        if not isinstance(content, str):
            raise ValueError("Некорректное описание места пользователя")

        return cls(_id_workstation=id_workstation, _number=number, _content_workstation=content)

    @classmethod
    def create(cls, number: int, content_workstation: str = None):
        id_workstation = id_gen.get_next_workstation_id()

        if not isinstance(number, int) or number < 0:
            raise ValueError("Некорректный номер места пользователя")
        if not isinstance(content_workstation, str):
            raise ValueError("Некорректное описание места пользователя")
        content_workstation = content_workstation or ""
        return cls(id_workstation, number, content_workstation or "")

    @property
    def id(self)-> int:
        return self._id_workstation

    @property
    def number(self)-> int:
        return self._number

    @property
    def content_workstation(self) -> str:
        return self._content_workstation

    @content_workstation.setter
    def content_workstation(self, new_content: str):
        if not isinstance(new_content, str): # проверяет, что значение совпадает с типом
            raise TypeError ("Значение должно быть строкой.")
        if not new_content.strip(): # удалила пробелы и если пусто то ошибка
            raise TypeError("Значение не может быть пустым.")
        self._content_workstation = new_content

