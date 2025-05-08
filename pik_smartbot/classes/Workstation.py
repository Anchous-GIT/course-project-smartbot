from dataclasses import dataclass

@ dataclass
class Workstation:
    _id: int
    _number: int
    _content_workstation: str

    @property # изучила, поняла что в питоне его используют для инкапсуляции
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

