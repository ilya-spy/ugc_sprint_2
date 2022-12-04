from functools import lru_cache
from logging import getLogger
from typing import AsyncIterator

from aiokafka import AIOKafkaConsumer

from etl.models import WatchingProgressKafkaSchema as KafkaSchema

logger = getLogger(__name__)


class Extractor:
    def __init__(self, extractor: AIOKafkaConsumer):
        self.extractor = extractor

    @staticmethod
    def retrieve_ids(msg_key: bytes):
        raw = msg_key.decode()
        unquoted = raw.rstrip()[1:-1]
        user_id, movie_id = unquoted.split("_")
        return user_id, movie_id

    async def extract(self) -> AsyncIterator[KafkaSchema]:
        data = await self.extractor.getmany(timeout_ms=1000, max_records=10000000)
        for pt, msgs in data.items():
            for msg in msgs:
                try:
                    user_id, movie_id = self.retrieve_ids(msg_key=msg.key)
                    yield KafkaSchema(
                        frame=msg.value.decode(),
                        user_id=user_id,
                        movie_id=movie_id,
                        event_time=msg.timestamp,
                    )
                except Exception as e:
                    logger.error(e)
                    continue


@lru_cache
def get_extractor(extractor: AIOKafkaConsumer) -> Extractor:
    return Extractor(extractor=extractor)
