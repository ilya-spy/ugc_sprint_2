import os
from logging import config as logging_config

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# наименование всего приложения (набора микросервисов)
APP_NAME = "ugc_gate"

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KAFKA_INSTANCE = "ugc_kafka:9092"
