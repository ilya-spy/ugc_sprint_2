from logging import getLogger

from clickhouse_driver.errors import Error
from pydantic import ValidationError

from etl import extractor, loader, transformer

logger = getLogger(__name__)


class Manager:
    def __init__(
        self,
        extractor_obj: extractor.Extractor,
        transformer_obj: transformer.Transformer,
        loader_obj: loader.Loader,
    ):
        self.extractor_obj = extractor_obj
        self.transform_obj = transformer_obj
        self.loader_obj = loader_obj

    async def data_to_load(self):
        """Extract and transform etl message to clickhouse schema"""
        async for kafka_msg in self.extractor_obj.extract():
            if kafka_msg is not None:
                try:
                    yield self.transform_obj.transform(kafka_msg)
                except ValidationError:
                    logger.exception("Wrong message value format")
                except ValueError:
                    logger.exception("Wrong message key format")

    async def start(self):
        """Infinite loop for extracting, transforming and loading data from etl to clickhouse"""
        while True:
            data_to_load = self.data_to_load()
            try:
                await self.loader_obj.load(ch_msgs=data_to_load)
            except Error:
                logger.exception("ClickHouse error")
            else:
                await self.extractor_obj.kafka_client.commit()
