from functools import lru_cache

from models import KafkaSchema
from services.kafka_consumer import get_kafka_consumer


class Extractor:
    def __init__(self):
        self.extractor = await get_kafka_consumer()

    async def extract(self) -> KafkaSchema:
        async for msg in self.extractor:
            # todo: ограничить количество потребляемых сообщений
            user_id, movie_id = msg.value.split("_")
            yield KafkaSchema(
                frame=msg.value,
                user_id=user_id,
                movie_id=movie_id,
                event_time=msg.timestamp,
            )


@lru_cache
def get_extractor():
    return Extractor()
