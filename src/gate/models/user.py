"""Классы описывающие модель данных Пользователь API и все связанные с ним модели.
"""

from pydantic import UUID4

from models.base import BaseModel


class UserRole(BaseModel):
    """Модель жанра"""

    id: UUID4
    name: str


class User(BaseModel):
    id: UUID4
    username: str
    email: str
