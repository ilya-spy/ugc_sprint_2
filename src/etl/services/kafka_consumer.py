from functools import lru_cache

from aiokafka import AIOKafkaConsumer

from config import config


@lru_cache
async def get_kafka_consumer() -> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        config.kafka.watching_progress_topic,
        bootstrap_servers=f"{config.kafka.host}:{config.kafka.port}",
        group_id=config.kafka.consumer_group_id,
    )

    await consumer.start()

    return consumer
