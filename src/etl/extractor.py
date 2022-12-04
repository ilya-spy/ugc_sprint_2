from functools import lru_cache
from logging import getLogger
from typing import AsyncIterator

from aiokafka import AIOKafkaConsumer

from etl.models import WatchingProgressKafkaSchema as KafkaSchema

logger = getLogger(__name__)


class Extractor:
    def __init__(self, extractor: AIOKafkaConsumer):
        self.extractor = extractor

    async def extract(self) -> AsyncIterator[KafkaSchema]:
        """Extracting batch of etl messages"""
        data = await self.extractor.getmany(timeout_ms=1000, max_records=10000000)
        for pt, msgs in data.items():
            for msg in msgs:
                try:
                    yield KafkaSchema(
                        value=msg.value, key=msg.key, event_time=msg.timestamp
                    )
                except Exception as e:
                    logger.error(e)
                    continue


@lru_cache
def get_extractor(extractor: AIOKafkaConsumer) -> Extractor:
    return Extractor(extractor=extractor)
