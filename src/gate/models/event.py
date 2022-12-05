from pydantic import UUID4

from models.base import BaseModel


class InputEvent(BaseModel):
    movie_id: UUID4
    frames: int
