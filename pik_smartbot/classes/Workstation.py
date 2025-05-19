from dataclasses import dataclass

@ dataclass
class Workstation:
    _id: int
    _number: int
    _content_workstation: str

    @classmethod
    def create(cls, id_workstation: int, number: int, content_workstation: str = None):
        if not isinstance(id_workstation, int) or id_workstation < 0:
            raise ValueError("Некорректный ID места")
        if not isinstance(number, int) or number < 0:
            raise ValueError("Некорректный номер места пользователя")
        if not isinstance(content_workstation, str):
            raise ValueError("Некорректное описание места пользователя")
        content_workstation = content_workstation or ""

    @property
    def id(self)-> int:
        return self._id

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

