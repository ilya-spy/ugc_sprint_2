import uuid
from functools import lru_cache

from etl import models


class Transformer:
    def transform(
        self,
        raw_msg: models.WatchingProgressKafkaSchema,
    ) -> models.WatchingProgressClickHouseSchema:
        """Transform etl messages to clickhouse table schema"""
        user_id, movie_id, frame = self._map_keys(raw_msg=raw_msg)
        return models.WatchingProgressClickHouseSchema(
            user_id=uuid.UUID(user_id),
            film_id=uuid.UUID(movie_id),
            frame=frame,
            event_time=raw_msg.event_time,
        )

    def _map_keys(self, raw_msg: models.WatchingProgressKafkaSchema):
        """Map kafka and clickhouse attributes"""
        user_id, movie_id = self._retrieve_ids(msg_key=raw_msg.key)
        frame = raw_msg.value.decode()
        return user_id, movie_id, frame

    @staticmethod
    def _retrieve_ids(msg_key: bytes):
        """Parse user_id and movie_id from etl message key"""
        raw = msg_key.decode()
        user_id, movie_id = raw.split("_")
        return user_id, movie_id


@lru_cache
def get_transformer() -> Transformer:
    """Singleton Transformer instance"""
    return Transformer()
