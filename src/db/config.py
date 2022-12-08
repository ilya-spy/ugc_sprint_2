import uuid

from pydantic import BaseSettings, Field


class OLAPSettings(BaseSettings):
    host: str = Field(default="localhost")
    port: int = Field(default=9000)
    cluster: str = Field(default="clickhouse")
    path: str = Field(default="/clickhouse/tables")
    db_default: str = Field(default="default")
    db_shard: str = Field(default="shard")
    db_replica: str = Field(default="replica")
    table: str = Field(default="main")
    scheme: str = Field(default="()")
    partition: str = Field(default="")
    orderby: str = Field(default="")
    populate: int = Field(default=0)

    class Config:
        env_prefix = "olap_views_"
        env_nested_delimiter = "_"


class KafkaConfig(BaseSettings):
    host: str = Field(default="localhost")
    port: str = Field(default="9092")
    batch_size: str = Field(default=10000000)
    consumer_group_id: str = Field(default_factory=uuid.uuid4)
    watching_progress_topic: str = Field(default="watching_progress")

    class Config:
        env_prefix = "kafka_"
