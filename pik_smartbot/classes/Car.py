from dataclasses import dataclass

@dataclass
class Car:
    _id_car: int
    _brand: str
    _model: str
    _number: str

    def to_dict(self) -> dict:
        return {
            "id": self._id_car,
            "brand": self._brand,
            "model": self._model,
            "number": self._number
        }

    @classmethod
    def from_dict(cls, data: dict):
        id_car = data.get("id")
        if not isinstance(id_car, int) or id_car < 0:
            raise ValueError("Invalid car ID")

        brand = data.get("brand")
        if not isinstance(brand, str) or not brand.strip():
            raise ValueError("Invalid car brand")

        model = data.get("model")
        if not isinstance(model, str) or not model.strip():
            raise ValueError("Invalid car model")

        number = data.get("number")
        if not isinstance(number, str) or not number.strip():
            raise ValueError("Invalid car number")

        return cls(id_car, brand, model, number)

    @classmethod
    def create(cls, id_car: int, brand: str, model: str, number: str):
        if not isinstance(id_car, int) or id_car < 0:
            raise ValueError("Некорректный ID машины")
        if not isinstance(brand, str) or not brand:
            raise ValueError("Некорректная марка машины")
        if not isinstance(model, str) or not model:
            raise ValueError("Некорректная модель машины")
        if not isinstance(number, str) or not number:
            raise ValueError("Некорректный номер машины")

        return cls(id_car, brand, model, number)

    @property
    def id(self) -> int:
        return self._id_car

    @property
    def brand(self) -> str:
        return self._brand

    @property
    def model(self) -> str:
        return   self._model

    @property
    def number(self)-> str:
        return self._number
