import json
from asyncio import Future
from typing import Iterable

from aiokafka import AIOKafkaProducer  # type: ignore

from utils.kafka.base import BaseProducer


class AIOProducer(BaseProducer):
    """Class for kafka producing management with aiokafka"""

    def __init__(self, aioproducer: AIOKafkaProducer):
        self._producer = aioproducer

    @property
    def producer(self) -> AIOKafkaProducer:
        return self._producer

    async def send(self, message, topic: str, *args, **kwargs) -> Future:
        """
        Method sends message to kafka topic with AIOKafka producer
        @param message: serializable message
        @param topic: topic name
        @param args: additional positional arguments for AIOKafkaProducer
        @param kwargs: additional keyword arguments for AIOKafkaProducer
        @return: Future related to message sending
        """
        fut = await self.producer.send(topic=topic)
        return fut

    async def send_and_wait(self, message: str, topic, *args, **kwargs) -> Future:
        """
        Method sends message to kafka topic with AIOKafka producer and waits until it will be delivered
        @param message: serializable message
        @param topic: topic name
        @param args: additional positional arguments for AIOKafkaProducer
        @param kwargs: additional keyword arguments for AIOKafkaProducer
        @return: Future related to message sending
        """
        fut = await self.producer.send_and_wait(
            message.encode("utf-8"), topic, *args, **kwargs
        )
        return fut

    async def send_batch(
        self, messages: Iterable[dict], topic, partition, *args, **kwargs
    ):
        """
        Method sends batch of message to kafka topic with AIOKafka producer
        @param partition: partition number
        @param messages: iterable consists of serializable messages
        @param topic: topic name
        @param args: additional positional arguments for AIOKafkaProducer
        @param kwargs: additional keyword arguments for AIOKafkaProducer
        @return: Future related to message sending
        """
        batch = self.producer.create_batch()

        for msg in messages:
            batch.append(
                value=json.dumps(msg, indent=4).encode("utf-8"),
                timestamp=None,
                key=None,
            )

        await self.producer.send_batch(batch=batch, topic=topic, partition=partition)
