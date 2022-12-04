from functools import lru_cache

from aiokafka import AIOKafkaConsumer

from etl.etl_config import get_config


@lru_cache
async def get_kafka_consumer() -> AIOKafkaConsumer:
    settings = get_config()

    consumer = AIOKafkaConsumer(
        "watching_progress",
        bootstrap_servers=f"{settings.kafka_host}:{settings.kafka_port}",
        auto_offset_reset="earliest",
        group_id="6",
    )

    await consumer.start()

    return consumer
