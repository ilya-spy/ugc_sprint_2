from extractor import get_extractor
from loader import get_loader
from transformer import get_transformer


class Administrator:
    def __init__(self):
        self.extractor = get_extractor()
        self.transform = get_transformer()
        self.loader = get_loader()

    async def start(self):
        while True:
            async for kafka_msg in self.extractor.extract():
                formatted_msg = self.transform.transform_unit(kafka_msg)
                await self.loader.load(ch_msg=formatted_msg)
