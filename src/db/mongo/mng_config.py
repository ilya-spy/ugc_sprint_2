import uuid

from pydantic import BaseSettings, Field


class MongoConfig(BaseSettings):
    host: str = Field(default="localhost")
    port: str = Field(default="9092")
    batch_size: str = Field(default=10000000)
    consumer_group_id: str = Field(default_factory=uuid.uuid4)
    likes_comments: str = Field(default="likes_comments")

    class Config:
        env_prefix = "mongo_"
