from functools import lru_cache
from logging import getLogger
from typing import AsyncIterator

from aiokafka import AIOKafkaConsumer  # type: ignore
from pydantic import ValidationError

from etl.models import WatchingProgressKafkaSchema as KafkaSchema

logger = getLogger(__name__)


class Extractor:
    def __init__(self, extractor: AIOKafkaConsumer):
        self.kafka_client = extractor

    async def extract(self) -> AsyncIterator[KafkaSchema]:
        """Extract batch of etl messages"""
        data = await self.kafka_client.getmany(timeout_ms=1000, max_records=10000000)
        for _, msgs in data.items():
            for msg in msgs:
                try:
                    yield KafkaSchema(
                        value=msg.value, key=msg.key, event_time=msg.timestamp
                    )
                except ValidationError:
                    logger.exception("Transforming error")


@lru_cache
def get_extractor(extractor: AIOKafkaConsumer) -> Extractor:
    """Singleton Extractor instance"""
    return Extractor(extractor=extractor)
