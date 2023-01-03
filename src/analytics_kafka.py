import asyncio
import json
import logging
import random
import time
import uuid

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, ConsumerRecord

from core.config import config
from utils.kafka import AIOConsumer, AIOProducer

logging.basicConfig()

NUM_INSERT = 10000
NUM_FETCH = 1000

logger = logging.getLogger("PERFORMANCE TEST RESULTS")
logger.setLevel(logging.INFO)


def get_id_filter(record: ConsumerRecord, id_):
    value = json.loads(record.value)

    if value.get("id") == id_:
        return True, False, value

    return False, False, value


async def get_consumer(topic_name):
    consumer = AIOKafkaConsumer(
        topic_name,
        bootstrap_servers=f"{config.kafka.host}:{config.kafka.port}",
        auto_offset_reset="earliest",
        enable_auto_commit=False,
    )
    await consumer.start()
    return consumer


async def main(topic_name):
    fetch_duration = 0
    insert_duration = 0
    prod = AIOProducer(
        aioproducer=AIOKafkaProducer(
            bootstrap_servers=f"{config.kafka.host}:{config.kafka.port}"
        )
    )
    await prod.producer.start()
    client_cons = await get_consumer(topic_name)
    cons = AIOConsumer(aioconsumer=client_cons)

    # insert data measure
    for j in range(NUM_FETCH):
        tac = time.perf_counter()
        await prod.send_batch(
            topic=TOPIC_NAME,
            partition=0,
            messages=(
                {
                    "id": i,
                    "film_id": str(uuid.uuid4()),
                    "user_id": str(uuid.uuid4()),
                    "rating": random.randint(0, 10),
                }
                for i in range(NUM_INSERT)
            ),
        )
        tic = time.perf_counter()

        insert_duration += tic - tac

        tac = time.perf_counter()
        id_ = random.randint(0, NUM_FETCH)
        await cons.filter(
            lambda x: get_id_filter(x, id_=id_),
            timeout_ms=60000,
            max_records=NUM_INSERT,
        )

        tic = time.perf_counter()

        fetch_duration += tic - tac

    logger.info("Fetching %s" % fetch_duration)
    logger.info("Insertion %s" % (insert_duration / NUM_FETCH))


if __name__ == "__main__":
    TOPIC_NAME = "kafka-performance-test"

    asyncio.run(main(topic_name=TOPIC_NAME))
