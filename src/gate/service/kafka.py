from functools import lru_cache


class KafkaService:
    def pub(self, data):
        pass


@lru_cache()
def get_kafka_service() -> KafkaService:
    return KafkaService()
