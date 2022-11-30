import uuid

from db.kafka_messaging.producers.base import BaseProducer


class WatchingProgressProducer(BaseProducer):
    @property
    def topic_name(self) -> str:
        return "user_watching_progress"

    def __init__(self):
        super(WatchingProgressProducer, self).__init__()

    def send(
        self,
        progress: str,
        user_id: uuid.UUID,
        movie_id: uuid.UUID,
        *args,
        **send_kwargs,
    ):
        super(WatchingProgressProducer, self).send(
            value=progress.encode(encoding="utf-8"),
            key=f"{user_id}_{movie_id}".encode(encoding="utf-8"),
        )
