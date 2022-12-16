import orjson
from pydantic import BaseModel


def orjson_dumps(values, *, default):
    """Десериализатор объекта в json строку"""
    return orjson.dumps(values, default=default).decode()


class BaseModel(BaseModel):
    """Базовый класс для всех Моделей данных. Переопределён сериализатор/десериализатор"""

    class Config:
        """Конфиг"""

        json_loads = orjson.loads
        json_dumps = orjson_dumps
