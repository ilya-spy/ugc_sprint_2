from logging import config as logging

from pydantic import BaseSettings, Field

from core.logger import LOGGING

# Применяем настройки логирования
logging.dictConfig(LOGGING)

# наименование всего приложения (набора микросервисов)
APP_NAME = "ugc_gate"

KAFKA_INSTANCE = "kafka:9092"


class KafkaConfig(BaseSettings):
    instance: str = Field(default="kafka:9092")

    class Config:
        env_prefix = "kafka_"


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

    kafka: KafkaConfig = KafkaConfig()
    auth_api: AuthAPIConfig = AuthAPIConfig()


class ProductionConfig(Config):
    """Конфиг для продакшена."""

    debug: bool = False
    app_config: str = "prod"


class DevelopmentConfig(Config):
    """Конфиг для девелопмент версии."""

    debug: bool = Field(default=True)


base_config = Config()
app_config = base_config.app_config

config: ProductionConfig | DevelopmentConfig
if app_config == "prod":
    config = ProductionConfig()
if app_config == "dev":
    config = DevelopmentConfig()
else:
    raise ValueError("Unknown environment stage")
