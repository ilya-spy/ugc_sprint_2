from logging import getLogger

logger = getLogger(__name__)


class Manager:
    def __init__(self, extractor, transformer, loader):
        self.extractor = extractor
        self.transform = transformer
        self.loader = loader

    async def data_to_load(self):
        """Extracting and transforming etl message to clickhouse schema"""
        async for kafka_msg in self.extractor.extract():
            if kafka_msg is not None:
                try:
                    yield self.transform.transform(kafka_msg)
                except Exception as e:
                    logger.error("TransformationError: %s" % e)

    async def start(self):
        """infinite loop for extracting, transforming and loading data from etl to clickhouse"""
        while True:
            data_to_load = self.data_to_load()
            try:
                await self.loader.load(ch_msgs=data_to_load)
            except Exception as e:
                logger.error("LoadingError: %s" % e)
