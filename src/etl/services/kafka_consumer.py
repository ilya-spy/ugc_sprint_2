from functools import lru_cache

from aiokafka import AIOKafkaConsumer
from etl_config import get_config


@lru_cache
async def get_kafka_consumer() -> AIOKafkaConsumer:
    settings = get_config()

    consumer = AIOKafkaConsumer(
        bootstrap_servers=f"{settings.kafka_host}:{settings.kafka_port}"
    )

    await consumer.start()

    return consumer
