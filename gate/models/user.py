"""Классы описывающие модель данных Пользователь API и все связанные с ним модели.
"""

from models.base import BaseModel
from pydantic import UUID4


class UserRole(BaseModel):
    """Модель жанра"""

    id: UUID4
    name: str


class User(BaseModel):
    id: UUID4
    username: str
    email: str
