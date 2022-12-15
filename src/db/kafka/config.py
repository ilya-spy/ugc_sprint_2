import uuid

from pydantic import BaseSettings, Field


class KafkaConfig(BaseSettings):
    host: str = Field(default="kafka")
    port: str = Field(default="9092")
    instance: str = Field(default="kafka:9092")

    batch_size: str = Field(default=10000000)
    consumer_group_id: str = Field(default_factory=uuid.uuid4)
    watching_progress_topic: str = Field(default="watching_progress")

    class Config:
        env_prefix = "kafka_"
