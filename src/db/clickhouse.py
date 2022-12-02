import abc
import logging
from dataclasses import dataclass, field
from typing import List

from clickhouse_driver import Client
from etl_config import setup_logger

logger = logging.getLogger(__name__)
logger = setup_logger(logger)


@dataclass
class IDistributedOLAPTable:
    """Класс-структура для хранения и передачи описания распределенных таблиц"""

    COLUMN_INT32 = "Int32"
    COLUMN_INT64 = "Int64"
    COLUMN_DATETIME = "DateTime"
    COLUMN_TYPES = [COLUMN_INT32, COLUMN_INT64, COLUMN_DATETIME]

    name: str
    schema: str = field(default="(id UUID)")
    partition: str = field(default="id")
    replica: str = field(default="default")
    root: str = field(default="/clickhouse/tables/")
    shard: str = field(default="default")
    key: str = field(default="id")

    def __post_init__(self):
        """Вычислить дополнительные поля после инициализации основных"""

        # Имена колонок без типов, для формирвоания запросов на чтение/запись
        if not hasattr(self, "columns"):
            self.columns = self.schema
            for column_type in self.COLUMN_TYPES:
                self.columns = self.columns.replace(column_type, "")


@dataclass
class IDistributedOLAPData:
    """Класс-структура для хранения и передачи кортежей данных в распределенных таблицах"""

    values: List[str]

    def __post_init__(self):
        """Вычислить дополнительные поля после инициализации основных"""

        # Массив данных, сериализованный в строку для записи в SQL
        self.serialized = ",".join(self.values)


@dataclass
class ClickHouseMergeTable(IDistributedOLAPTable):
    engine: str = field(default="MergeTree()")


@dataclass
class ClickHouseDistributedProxyTable(IDistributedOLAPTable):
    cluster: str = field(default="clickhouse")

    def __post_init__(self):
        """Вычислить дополнительные поля после инициализации основных"""
        super().__post_init__()

        self.engine = f"Distributed('{self.cluster}', '', {self.name}, rand())"

        # Выключить генерацию расширенного CREATE TABLE, для прокси он не используются
        self.partition = None
        self.key = None


@dataclass
class ClickHouseReplicatedTable(IDistributedOLAPTable):
    def __post_init__(self):
        """Вычислить дополнительные поля после инициализации основных"""
        super().__post_init__()

        self.engine = f"ReplicatedMergeTree('{self.root}/{self.shard}/{self.name}', '{self.replica}')"


class IDistributedOLAPClient(abc.ABC):
    """Интерфейс доступа в распределенные ОЛАП-хранилища"""

    @abc.abstractmethod
    def show_databases(self):
        """Показать список доступных на сервере баз"""

    @abc.abstractmethod
    def create_distributed_db(self, db: str):
        """Создание новой распределенной базы"""

    @abc.abstractmethod
    def create_distributed_table(self, db: str, table: IDistributedOLAPTable):
        """Создание новой распределенной таблицы"""

    @abc.abstractmethod
    def insert_into_table(
        self, db: str, table: IDistributedOLAPTable, data: IDistributedOLAPData
    ):
        """Вставка данных распределенной таблицы"""

    @abc.abstractmethod
    def fetch_table(self, db: str, table: IDistributedOLAPTable):
        """Выборка всех данных распределенной таблицы"""


class ClickHouseClient(IDistributedOLAPClient):
    """Класс-библиотека методов для реализация распределенного ОЛАП-интерфейса на основе ClickHouse"""

    def __init__(
        self, host: str = "localhost", port: int = 9000, cluster: str = "default"
    ) -> None:
        """Создать экземпляр клиента ClickHouse и подключиться к серверу контейнера СУБД"""
        super().__init__()
        self.host = host
        self.port = port
        self.cluster = cluster

        self.client = Client(host=self.host, port=self.port)

    def show_databases(self):
        operator = "SHOW DATABASES"
        return self.client.execute(operator)

    def create_distributed_db(self, db: str):
        operator = f"CREATE DATABASE IF NOT EXISTS {db} ON CLUSTER {self.cluster}"
        return self.client.execute(operator)

    def create_distributed_table(self, db: str, table: IDistributedOLAPTable):
        operator = f"CREATE TABLE IF NOT EXISTS {db}.{table.name}"
        header = f"{table.schema} Engine={table.engine}"
        logger.debug("%s %s", operator, header)

        partition = f"PARTITION BY {table.partition}" if table.partition else ""
        order = f"ORDER BY {table.key}" if table.key else ""

        result = self.client.execute(" ".join([operator, header, partition, order]))
        return result

    def insert_into_table(
        self, db: str, table: IDistributedOLAPTable, data: IDistributedOLAPData
    ):
        operator = f"INSERT INTO {db}.{table.name} {table.columns}"
        data = f"VALUES {data.serialized}"

        logger.debug(operator)
        logger.debug(data)

        result = self.client.execute(" ".join([operator, data]))
        return result

    def fetch_table(self, db: str, table: IDistributedOLAPTable):
        result = self.client.execute(f"SELECT * FROM {db}.{table.name}")
        return result
