from db.kafka_messaging.consumers.base import BaseConsumer


class WatchingProgBaseConsumer(BaseConsumer):
    @property
    def topic_name(self) -> str:
        return "user_watching_progress"

    def __init__(self):
        super(WatchingProgBaseConsumer, self).__init__()
