from extension.kafka_setting import BootstrapServersReferenceMixin as BootstrapServers
from abc import abstractmethod, ABC
from kafka import KafkaConsumer


class BaseConsumer(BootstrapServers, ABC):
    @property
    @abstractmethod
    def topic_name(self) -> str:
        """Topic where to produce"""

    @property
    @abstractmethod
    def group_id(self) -> str:
        pass

    def __init__(self):
        self.consumer = KafkaConsumer(
            self.topic_name,
            auto_offset_reset='earliest',
            group_id=self.group_id,
            bootstrap_servers=self.bootstrap_servers
        )

    def consume(self):
        return next(self.consumer)
