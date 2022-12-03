class Manager:
    def __init__(self, extractor, transformer, loader):
        self.extractor = extractor
        self.transform = transformer
        self.loader = loader

    async def start(self):
        while True:
            async for kafka_msg in self.extractor.extract():
                formatted_msg = self.transform.transform_unit(kafka_msg)
                self.loader.load(ch_msg=formatted_msg)
