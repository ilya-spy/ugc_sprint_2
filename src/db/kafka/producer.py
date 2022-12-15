import asyncio

from functools import lru_cache

from aiokafka import AIOKafkaProducer

from core.config import config


@lru_cache
def get_kafka_producer() -> AIOKafkaProducer:
    loop = asyncio.get_event_loop()

    producer = AIOKafkaProducer(
        loop=loop, client_id=config.app_name, bootstrap_servers=[config.kafka.instance]
    )
    return producer
