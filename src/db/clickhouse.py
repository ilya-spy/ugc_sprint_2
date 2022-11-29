import abc
import logging
from dataclasses import dataclass, field
from typing import List

from clickhouse_driver import Client

from config import setup_logger


logger = logging.getLogger(__name__)
logger = setup_logger(logger)

@dataclass
class IDistributedOLAPTable:
    """Класс-структура для хранения и передачи описания распределенных таблиц"""

    COLUMN_INT32    = 'Int32'
    COLUMN_INT64    = 'Int64'
    COLUMN_DATETIME = 'DateTime'
    COLUMN_TYPES    = [COLUMN_INT32, COLUMN_INT64, COLUMN_DATETIME]

    name: str
    schema: str
    partition: str
    replica: str
    root: str
    shard: str
    key: str

    engine: str

    def __post_init__(self):
        """Вычислить дополнительные поля после инициализации основных"""
        
        # Имена колонок без типов, для формирвоания запросов на чтение/запись
        self.columns = self.schema
        for column_type in self.COLUMN_TYPES:
            self.columns = self.columns.replace(column_type, '')

        self.columns = self.columns.split(',')


@dataclass
class IDistributedOLAPData:
    """Класс-структура для хранения и передачи кортежей данных в распределенных таблицах"""
    values: List[str]

    def __post_init__(self):
        """Вычислить дополнительные поля после инициализации основных"""

        # Массив данных, сериализованный в строку для записи в SQL
        self.serialized = ','.join(self.values)


@dataclass
class ClickHouseMergeTable(IDistributedOLAPTable):
    engine: str = field(default='MergeTree()')


@dataclass
class ClickHouseReplicatedTable(ClickHouseMergeTable):
    def __post_init__(self):
        """Вычислить дополнительные поля после инициализации основных"""
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
    def insert_into_table(self, db: str, table: IDistributedOLAPTable, data: IDistributedOLAPData):
        """Вставка данных распределенной таблицы"""

    @abc.abstractmethod
    def fetch_table(self, db: str, table: IDistributedOLAPTable):
        """Выборка всех данных распределенной таблицы"""


class ClickHouseClient(IDistributedOLAPClient):
    """Класс-библиотека методов для реализация распределенного ОЛАП-интерфейса на основе ClickHouse"""

    def __init__(self, host: str ='localhost', port: int =9000, cluster: str ='default') -> None:
        """Создать экземпляр клиента ClickHouse и подключиться к серверу контейнера СУБД"""
        super().__init__()
        self.host = host
        self.port = port
        self.cluster = cluster

        self.client = Client(host=self.host, port=self.port)

    def show_databases(self):
        operator = f'SHOW DATABASES'
        return self.client.execute(operator)

    def create_distributed_db(self, db: str):
        operator = f'CREATE DATABASE IF NOT EXISTS {db} ON CLUSTER {self.cluster}'
        return self.client.execute(operator)

    def create_distributed_table(self, db: str, table: IDistributedOLAPTable):
        operator = f'CREATE TABLE IF NOT EXISTS {db}.{table.name} ON CLUSTER {self.cluster}'
        logger.info(operator)
        table = f'{table.schema} Engine={table.engine} PARTITION BY {table.partition} ORDER BY {table.key}'
        logger.info(table)

        result = self.client.execute(' '.join([operator, table]))
        return result

    def insert_into_table(self, db: str, table: IDistributedOLAPTable, data: IDistributedOLAPData):
        operator = f'INSERT INTO {db}.{table.name} {",".join(table.columns)}'
        data = f'VALUES {data.serialized}'
        
        result = self.client.execute(' '.join([operator, data]))
        return result

    def fetch_table(self, db: str, table: IDistributedOLAPTable):
        result = self.client.execute(f'SELECT * FROM {db}.{table.name}')
        return result
