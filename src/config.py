import logging
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


class Config(BaseSettings):
    """Настройки приложения."""

    app_name: str = Field(default="views_oltp_olap")
    app_config: str = Field(default="dev")
    debug: bool = Field(default=True)
    loglevel: str = Field(default="DEBUG")

    olap: OLAPSettings = OLAPSettings()
    kafka: KafkaConfig = KafkaConfig()


class ProductionConfig(Config):
    """Конфиг для продакшена."""

    debug: bool = False
    app_config: str = "prod"


class DevelopmentConfig(Config):
    """Конфиг для девелопмент версии."""

    debug: bool = Field(default=True)


base_config = Config()
app_config = base_config.app_config

if app_config == "prod":
    config = ProductionConfig()
if app_config == "dev":
    config = DevelopmentConfig()
else:
    raise ValueError("Unknown environment stage")


def setup_logger(logger: logging.Logger):
    # Create logging handlers
    c_handler = logging.StreamHandler()

    # Create formatters and add it to handlers
    c_format = logging.Formatter("%(name)s - %(levelname)s: %(message)s")
    c_handler.setFormatter(c_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.setLevel(config.loglevel)

    return logger
