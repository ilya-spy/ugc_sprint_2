import uuid
from typing import Optional

from pydantic import BaseSettings, Field


class KafkaConfig(BaseSettings):
    host: Optional[str] = Field(default="localhost")
    port: Optional[str] = Field(default="29092")
    instance: Optional[str] = Field(default="localhost:29092")

    batch_size: Optional[str] = Field(default=10000000)
    consumer_group_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    watching_progress_topic: Optional[str] = Field(default="watching_progress")

    class Config:
        env_prefix = "kafka_"
