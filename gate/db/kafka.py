from typing import Optional

from aiokafka import AIOKafkaProducer

producer: Optional[AIOKafkaProducer] = None


# Функция понадобится при внедрении зависимостей
async def get_kafka() -> AIOKafkaProducer:
    return producer
