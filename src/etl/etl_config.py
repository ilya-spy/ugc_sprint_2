from functools import lru_cache

from pydantic import BaseConfig


class ETLConfig(BaseConfig):
    kafka_host: str
    kafka_port: str


@lru_cache
def get_config() -> ETLConfig:
    return ETLConfig()
