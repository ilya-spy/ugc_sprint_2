from typing import Final
from uuid import uuid4

from api.models._base_model import USER_ID  # type: ignore
from fastapi import Query
from fastapi.params import Query as QueryInstance
from pydantic import Required

MOVIE_ID: Final[QueryInstance] = Query(
    alias="movie_id",
    title="UUID",
    default=Required,
    example=uuid4(),
    description="ID фильма из бд",
)

LAST_FRAME: Final[QueryInstance] = Query(
    alias="last_frame",
    title="Размер страницы",
    default=Required,
    ge=0,
    description="Кол-во элементов на странице",
)


class FilmEventParams:
    def __init__(
        self,
        user_id: str = USER_ID,  # type: ignore
        movie_id: str = MOVIE_ID,  # type: ignore
        last_frame: int = LAST_FRAME,  # type: ignore
    ) -> None:
        self.user_id = user_id
        self.movie_id = movie_id
        self.last_frame = last_frame
