import abc


class BaseProducer(abc.ABC):
    @property
    @abc.abstractmethod
    def producer(self):
        """Property that produces messages"""
        pass

    @abc.abstractmethod
    async def send(self, *args, **kwargs):
        """Method sends message to kafka"""
        pass

    @abc.abstractmethod
    def send_batch(self, *args, **kwargs):
        """Method sends message group to kafka"""
        pass


class BaseConsumer(abc.ABC):
    @property
    @abc.abstractmethod
    def consumer(self):
        """Property that consumes messages"""
        pass

    @abc.abstractmethod
    async def consume(self):
        """Method consumes messages to kafka"""
        pass
