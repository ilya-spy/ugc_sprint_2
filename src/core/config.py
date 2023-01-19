from typing import Optional, Union

from pydantic import BaseSettings, Field

from db.clickhouse.ch_config import ClickHouseConfig
from db.kafka.kfk_config import KafkaConfig
from db.mongo.mng_config import MongoDBConfig


class SentryConfig(BaseSettings):
    dsn: Optional[str]

    class Config:
        env_prefix = "sentry_"


class AuthAPIConfig(BaseSettings):
    address: str = Field(default="http://auth_api:8000/")

    class Config:
        env_prefix = "auth_api_"


class Config(BaseSettings):
    """Настройки приложения."""

    app_name: str = Field(default="ugc_gate")
    app_config: str = Field(default="dev")
    debug: bool = Field(default=True)
    loglevel: str = Field(default="DEBUG")

    olap: ClickHouseConfig = ClickHouseConfig()
    kafka: KafkaConfig = KafkaConfig()
    auth_api: AuthAPIConfig = AuthAPIConfig()
    sentry: SentryConfig = SentryConfig()
    mongo: MongoDBConfig = MongoDBConfig()


class ProductionConfig(Config):
    """Конфиг для продакшена."""

    debug: bool = False
    app_config: str = "prod"


class DevelopmentConfig(Config):
    """Конфиг для девелопмент версии."""

    debug: bool = Field(default=True)


# Choose default config
app_config = Config().app_config

config: Union[ProductionConfig, DevelopmentConfig]
if app_config == "prod":
    config = ProductionConfig()
if app_config == "dev":
    config = DevelopmentConfig()
else:
    raise ValueError("Unknown environment stage")
