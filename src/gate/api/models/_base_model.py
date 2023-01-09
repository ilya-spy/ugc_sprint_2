from http import HTTPStatus
from typing import Final
from uuid import uuid4

import orjson
from fastapi import Query
from fastapi.params import Query as QueryInstance
from orjson import loads
from pydantic import BaseModel, Field, Required


def orjson_dumps(obj, *, default):
    return orjson.dumps(
        obj,
        default=default,
    ).decode()


class ORJSONBase(BaseModel):
    class Config:
        json_loads = loads
        json_dumps = orjson_dumps

        use_enum_values = True


class AbstractModel(ORJSONBase):

    id: str = Field(default_factory=uuid4)
    created_at: str


class BookmarkRecord(BaseModel):
    user_id: str
    movie_id: str


class LikeRecord(BookmarkRecord):
    ...


class RatingRecord(LikeRecord):
    rating: int = Field(ge=1, le=10)


class Response(ORJSONBase):

    status: HTTPStatus
    message: str


USER_ID: Final[QueryInstance] = Query(
    alias="user_id",
    title="UUID",
    default=Required,
    example=uuid4(),
    description="ID пользователя из бд",
)

RATING_SCORE: Final[QueryInstance] = Query(
    alias="rating",
    title="Оценка фильма",
    ge=1,
    le=10,
    description="Оценка поставленная пользователем фильму",
)
