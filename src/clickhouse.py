import abc

from clickhouse_driver import Client


class IDistributedOLAPClient(abc.ABC):
    """Интерфейс доступа в распределенные ОЛАП-хранилища"""
    @abc.abstractmethod
    def show_databases(self):
        """Показать список доступных на сервере баз"""

    @abc.abstractmethod
    def create_distributed_db(self, db: str):
        """Создание новой распределенной базы"""
    
    @abc.abstractmethod
    def create_distributed_table(self, db: str, table: str, columns: str):
        """Создание новой распределенной таблицы"""

    @abc.abstractmethod
    def insert_into_distributed_table(self, db: str, table: str, columns: str, values: str):
        """Вставка данных распределенной таблицы"""

    @abc.abstractmethod
    def drop_distributed_db(self, db: str):
        """Удвление существующей распределенной базы"""


class ClickHouseClient(IDistributedOLAPClient):
    """Класс-библиотека методов для реализация распределенного ОЛАП-интерфейса на основе ClickHouse"""

    def __init__(self, host='localhost', port=9000) -> None:
        """Создать экземпляр клиента ClickHouse и подключиться к серверу контейнера СУБД"""
        super().__init__()
        self.client = Client(host)

    def show_databases(self):
        result = self.client.execute('SHOW DATABASES')
        return result

    def create_distributed_db(self, db: str):
        result = self.client.execute(f'CREATE DATABASE IF NOT EXISTS {db} ON CLUSTER company_cluster')
        return result
    
    def create_distributed_table(self, db: str, table: str, columns: str = '(id Int64, x Int32) '):
        result = self.client.execute(f'CREATE TABLE {db}.{table} ON CLUSTER company_cluster {columns} Engine=MergeTree() ORDER BY id')
        return result

    def insert_into_distributed_table(self, db: str, table: str, columns: str, values: str):
        result = self.client.execute(f'INSERT INTO {db}.{table} {columns} VALUES {values}')
        return result

    def drop_distributed_table(self, name: str):
        pass
