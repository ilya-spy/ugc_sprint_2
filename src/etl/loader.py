from functools import lru_cache


class Loader:
    def __init__(self):
        self.ch_client = ...

    async def load(self, ch_msg):
        ...


@lru_cache
def get_loader() -> Loader:
    return Loader()
