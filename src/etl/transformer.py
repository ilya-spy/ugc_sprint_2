from functools import lru_cache
from typing import Iterator

from models import ClickHouseSchema, KafkaSchema


class Transformer:
    def transform(self, raw_messages: Iterator[KafkaSchema]) -> ClickHouseSchema:
        for msg in raw_messages:
            yield self.transform_unit(raw_msg=msg)

    @staticmethod
    def transform_unit(raw_msg: KafkaSchema) -> ClickHouseSchema:
        return ClickHouseSchema(
            user_id=raw_msg.user_id,
            film_id=raw_msg.film_id,
            frame=raw_msg.frame,
            event_time=raw_msg.event_time,
        )


@lru_cache
def get_transformer() -> Transformer:
    return Transformer()
