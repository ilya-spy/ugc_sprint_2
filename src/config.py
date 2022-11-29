import os
import logging

from pydantic import BaseSettings, Field


class OLAPSettings(BaseSettings):
    cluster: str = Field(default='clickhouse')
    path: str = Field(default='/clickhouse/tables')
    table: str = Field(default='main')
    scheme: str = Field(default='()')
    partition: str = Field(default='')
    orderby: str = Field(default='')

    class Config:
        env_prefix = 'olap_views_'
        env_nested_delimiter = '_'


class Config(BaseSettings):
    """Настройки приложения."""

    app_name: str = Field(default='views_oltp_olap')
    app_config: str = Field(default='dev')
    debug: bool = Field(default=True)
    loglevel: str = Field(default='DEBUG')

    olap: OLAPSettings = OLAPSettings()


class ProductionConfig(Config):
    """Конфиг для продакшена."""
    debug: bool = False
    app_config: str = 'prod'


class DevelopmentConfig(Config):
    """Конфиг для девелопмент версии."""
    debug: bool = Field(default=True)



base_config = Config()
app_config = base_config.app_config

if app_config == "prod":
    config = ProductionConfig()
if app_config == "dev":
    config = DevelopmentConfig()

def setup_logger(logger: logging.Logger):
    # Create logging handlers
    c_handler = logging.StreamHandler()

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s: %(message)s')
    c_handler.setFormatter(c_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.setLevel(config.loglevel)

    return logger

if __name__ == '__main__':
    from pprint import pprint
    pprint('### Application configuration: \n')
    pprint(config().dict())
