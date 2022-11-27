import abc

from clickhouse_driver import Client


class IDistributedOLAPClient(abc.ABC):
    """Интерфейс доступа в распределенные ОЛАП-хранилища"""
    @abc.abstractmethod
    def show_databases(self):
        """Показать список доступных на сервере баз"""

    @abc.abstractmethod
    def create_distributed_table(self, name: str):
        """Создание новой распределенной таблицы"""

    @abc.abstractmethod
    def drop_distributed_table(self, name: str):
        """Удвление существующей распределенной таблицы"""


class ClickHouseClient(IDistributedOLAPClient):
    """Класс-библиотека методов для реализация распределенного ОЛАП-интерфейса на основе ClickHouse"""

    def __init__(self, host='localhost', port=9000) -> None:
        """Создать экземпляр клиента ClickHouse и подключиться к серверу контейнера СУБД"""
        super().__init__()

        self.client = Client(host)

    def show_databases(self):
        result = self.client.execute('SHOW DATABASES')
        return result

    def create_distributed_table(self, name: str):
        pass

    def drop_distributed_table(self, name: str):
        pass
