from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class KafkaSchema(BaseModel):
    frame: int = Field(title="единица просмотра фильма")
    user_id: UUID = Field(title="идентификатор пользователя")
    film_id: UUID = Field(title="идентификатор фильма")
    event_time: datetime = Field(title="время появления события в кафка")


class ClickHouseSchema(BaseModel):
    user_id: UUID = Field(title="идентификатор пользователя")
    film_id: UUID = Field(title="идентификатор фильма")
    frame: int = Field(title="единица просмотра фильма")
    event_time: datetime = Field(title="время фиксации события")
