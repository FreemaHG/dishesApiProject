from pydantic import field_validator

from src.schemas.base import BaseOutSchema, BaseInSchema


class DishInSchema(BaseInSchema):
    """
    Схема для добавления нового блюда
    """
    price: float


class DishOutSchema(BaseOutSchema):
    """
    Схема для вывода блюда
    """
    price: str

    @field_validator("price", mode="before")
    def serialize_price(cls, val: float):
        """
        Возвращаем цену блюда в виде строки с округлением до двух знаков после запятой
        """
        return "%.2f" % val
