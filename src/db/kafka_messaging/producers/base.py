from abc import ABC, abstractmethod

from kafka import KafkaProducer

from extension.kafka_setting import BootstrapServers as BootstrapServers


class BaseProducer(BootstrapServers, ABC):
    @property
    @abstractmethod
    def topic_name(self) -> str:
        """Topic where to produce"""

    def __init__(self):
        self.prod = KafkaProducer(bootstrap_servers=self.bootstrap_servers)

    def send(self, *args, **send_kwargs):
        self.prod.send(topic=self.topic_name, *args, **send_kwargs)
