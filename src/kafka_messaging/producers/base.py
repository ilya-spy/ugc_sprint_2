from extension.kafka_setting import BootstrapServersReferenceMixin as BootstrapServers
from abc import abstractmethod, ABC
from kafka import KafkaProducer


class BaseProducer(BootstrapServers, ABC):
    @property
    @abstractmethod
    def topic_name(self) -> str:
        """Topic where to produce"""

    def __init__(self):
        self.prod = KafkaProducer(bootstrap_servers=self.bootstrap_servers)

    def send(self, *args, **send_kwargs):
        self.prod.send(topic=self.topic_name, *args, **send_kwargs)
