from pydantic import BaseSettings, Field

from db.config import OLAPSettings
from db.config import KafkaConfig

class Config(BaseSettings):
    """Настройки приложения."""

    app_name: str = Field(default="ugc_services")
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


# Choose default config
app_config = Config().app_config

if app_config == "prod":
    config = ProductionConfig()
if app_config == "dev":
    config = DevelopmentConfig()
else:
    raise ValueError("Unknown environment stage")


