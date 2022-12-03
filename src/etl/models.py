import uuid
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class WatchingProgressKafkaSchema:
    frame: int  # единица просмотра фильма
    user_id: UUID  # идентификатор пользователя
    movie_id: UUID  # идентификатор фильма
    event_time: int | float  # время появления события в кафка

    def __post_init__(self):
        self.event_time = (
            self.event_time / 1000 if self.event_time is not None else None
        )


@dataclass
class WatchingProgressClickHouseSchema:
    user_id: uuid.UUID
    film_id: uuid.UUID
    frame: int
    event_time: datetime
