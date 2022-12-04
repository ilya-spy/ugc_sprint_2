from functools import lru_cache

from etl import models


class Transformer:
    @staticmethod
    def transform(
        raw_msg: models.WatchingProgressKafkaSchema,
    ) -> models.WatchingProgressClickHouseSchema:
        return models.WatchingProgressClickHouseSchema(
            user_id=raw_msg.user_id,
            film_id=raw_msg.movie_id,
            frame=raw_msg.frame,
            event_time=raw_msg.event_time,
        )


@lru_cache
def get_transformer() -> Transformer:
    return Transformer()
