import json
from functools import lru_cache

from fastapi import Depends

from db.kafka import get_kafka, AIOKafkaProducer


class EventStorageService:
    def __init__(self, kafka: AIOKafkaProducer):
        self.kafka = kafka

    async def send(self, topic_name: str, partition_name: str, data: dict) -> None:
        await self.kafka.send(
            topic=topic_name,
            partition=partition_name,
            value=json.dumps(data).encode("ascii")
        )

        return None


@lru_cache()
def get_event_storage_service(
    kafka: AIOKafkaProducer = Depends(get_kafka)
) -> EventStorageService:
    return EventStorageService(kafka)
