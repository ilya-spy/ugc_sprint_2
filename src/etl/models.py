import uuid
from typing import Union

from pydantic import BaseModel, Field, validator


class WatchingProgressKafkaSchema(BaseModel):
    value: bytes
    key: bytes
    event_time: Union[int, float]

    @validator("event_time", pre=True, always=True)
    def timestamp_to_ms(cls, value):
        """Convert timestamp to ms"""
        if value is not None:
            value /= 1000
        return value


class WatchingProgressClickHouseSchema(BaseModel):
    user_id: uuid.UUID
    film_id: uuid.UUID
    frame: int = Field(gt=0)
    event_time: Union[int, float]
