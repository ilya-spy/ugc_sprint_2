from abc import ABC, abstractmethod

from kafka import KafkaConsumer

from extension.kafka_setting import BootstrapServers


class BaseConsumer(BootstrapServers, ABC):
    @property
    @abstractmethod
    def topic_name(self) -> str:
        """Topic where to produce"""

    def __init__(self):
        self.consumer = KafkaConsumer(
            self.topic_name,
            auto_offset_reset="earliest",
            bootstrap_servers=self.bootstrap_servers,
        )

    def consume(self):
        return next(self.consumer)
