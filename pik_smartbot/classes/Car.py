from dataclasses import dataclass

@ dataclass
class Car:
    _id_car: int
    _brand: str
    _model: str
    _number_car: str

    @property
    def id_car(self) -> int:
        return self._id_car

    @property
    def brand(self) -> str:
        return self._brand

    @property
    def model(self) -> str:
        return self._model

    @property
    def number_car(self) -> str:
        return self._number_car
