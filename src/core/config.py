from pydantic import BaseSettings, Field

from db.clickhouse.ch_config import ClickHouseConfig
from db.kafka.kfk_config import KafkaConfig


class SentryConfig(BaseSettings):
    dsn: str

    class Config:
        env_prefix = "sentry_"


class Config(BaseSettings):
    """Настройки приложения."""

    app_name: str = Field(default="ugc_services")
    app_config: str = Field(default="dev")
    debug: bool = Field(default=True)
    loglevel: str = Field(default="DEBUG")

    olap: ClickHouseConfig = ClickHouseConfig()
    kafka: KafkaConfig = KafkaConfig()
    sentry: SentryConfig = SentryConfig()


class ProductionConfig(Config):
    """Конфиг для продакшена."""

    debug: bool = False
    app_config: str = "prod"


class DevelopmentConfig(Config):
    """Конфиг для девелопмент версии."""

    debug: bool = Field(default=True)


# Choose default config
app_config = Config().app_config

config: ProductionConfig | DevelopmentConfig
if app_config == "prod":
    config = ProductionConfig()
if app_config == "dev":
    config = DevelopmentConfig()
else:
    raise ValueError("Unknown environment stage")
