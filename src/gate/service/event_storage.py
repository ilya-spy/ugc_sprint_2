from functools import lru_cache

from fastapi import Depends
from models.event import KafkaEvent

from db.kafka.producer import AIOKafkaProducer, get_kafka_producer


class EventStorageService:
    def __init__(self, kafka: AIOKafkaProducer):
        self.kafka = kafka

    async def send(self, topic_name: str, model: KafkaEvent):
        """Send  message to kafka topic"""
        await self.kafka.send(topic=topic_name, key=model.key, value=model.value)


@lru_cache
def get_event_storage_service(
    kafka: AIOKafkaProducer = Depends(get_kafka_producer),
) -> EventStorageService:
    """Singleton EventStorageService instance"""
    return EventStorageService(kafka)
