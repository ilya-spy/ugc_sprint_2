import asyncio
from functools import lru_cache

from aiokafka import AIOKafkaProducer  # type: ignore

from core.config import config


@lru_cache
def get_kafka_producer() -> AIOKafkaProducer:
    """Singleton async kafka producer"""
    loop = asyncio.get_event_loop()

    producer = AIOKafkaProducer(
        loop=loop, client_id=config.app_name, bootstrap_servers=[config.kafka.instance]
    )
    return producer
