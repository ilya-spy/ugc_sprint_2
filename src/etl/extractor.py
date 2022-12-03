from functools import lru_cache
from typing import AsyncIterator

from aiokafka import AIOKafkaConsumer

from etl.models import WatchingProgressKafkaSchema as KafkaSchema


class Extractor:
    def __init__(self, extractor: AIOKafkaConsumer):
        self.extractor = extractor

    def retrieve_ids(self, msg_key: bytes):
        raw = msg_key.decode()
        unquoted = raw[1:-1]
        user_id, movie_id = unquoted.split("_")
        return user_id, movie_id

    async def extract(self) -> AsyncIterator[KafkaSchema]:
        async for msg in self.extractor:
            # todo: ограничить количество потребляемых сообщений
            user_id, movie_id = self.retrieve_ids(msg_key=msg.key)
            yield KafkaSchema(
                frame=msg.value.decode(),
                user_id=user_id,
                movie_id=movie_id,
                event_time=msg.timestamp,
            )


@lru_cache
def get_extractor(extractor: AIOKafkaConsumer) -> Extractor:
    return Extractor(extractor=extractor)
