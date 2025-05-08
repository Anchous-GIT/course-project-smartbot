from dataclasses import dataclass

@ dataclass
class Car:
    _id: int
    _brand: str
    _model: str
    _number: str

    @property
    def id(self) -> int:
        return self._id

    @property
    def brand(self) -> str:
        return self._brand

    @property
    def model(self) -> str:
        return self._model

    @property
    def number(self)-> str:
        return self._number
