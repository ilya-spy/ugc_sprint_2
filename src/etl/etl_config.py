from functools import lru_cache

from pydantic import BaseSettings, Field


class ETLConfig(BaseSettings):
    kafka_host: str = Field(default="localhost")
    kafka_port: str = Field(default="29092")
    batch_size: int = Field(default=10)


@lru_cache
def get_config() -> ETLConfig:
    return ETLConfig()
