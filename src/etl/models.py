import uuid
from typing import Union

from pydantic import BaseModel, Field, validator


class WatchingProgressKafkaSchema(BaseModel):
    value: bytes
    key: bytes
    event_time: Union[int, float]

    @validator("event_time", pre=True, always=True)
    def timestamp_to_ms(cls, v):
        if v is not None:
            v /= 1000
        return v


class WatchingProgressClickHouseSchema(BaseModel):
    user_id: uuid.UUID
    film_id: uuid.UUID
    frame: int = Field(gt=0)
    event_time: Union[int, float]
