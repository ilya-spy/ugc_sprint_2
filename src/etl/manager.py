class Manager:
    def __init__(self, extractor, transformer, loader):
        self.extractor = extractor
        self.transform = transformer
        self.loader = loader

    async def data_to_load(self):
        async for kafka_msg in self.extractor.extract():
            if kafka_msg is not None:
                yield self.transform.transform(kafka_msg)

    async def start(self):
        while True:
            data_to_load = self.data_to_load()
            await self.loader.load(ch_msgs=data_to_load)
