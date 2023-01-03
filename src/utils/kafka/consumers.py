from typing import Callable

from aiokafka import AIOKafkaConsumer

from utils.kafka.base import BaseConsumer


class AIOConsumer(BaseConsumer):
    @property
    def consumer(self) -> AIOKafkaConsumer:
        return self._consumer

    def __init__(self, aioconsumer: AIOKafkaConsumer):
        self._consumer = aioconsumer

    async def consume(self):
        """Generator for message consumption"""
        async for msg in self.consumer:
            yield msg

    async def consume_batch(self, *partitions, message_number=10000, timeout=10000):
        result = await self.consumer.getmany(
            *partitions, timeout_ms=timeout, max_records=message_number
        )
        for _, messages in result:
            yield messages

    async def filter(self, filtering_func: Callable, *args, **kwargs):
        found = []
        data = await self.consumer.getmany(*args, **kwargs)
        for result in data:
            for record in data[result]:
                status, stop, entity = filtering_func(record)
                if status:
                    found.append(entity)
                if stop:
                    break
        return found
