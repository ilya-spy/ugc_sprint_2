from fastapi import APIRouter, Depends

from api.schemas.common import DefaultSuccessResponse
from service.kafka import KafkaService, get_kafka_service

router = APIRouter()


@router.get(path="/", response_model=DefaultSuccessResponse)
async def save(
    kafka_service: KafkaService = Depends(get_kafka_service)
) -> DefaultSuccessResponse:
    # kafka_service.pub(data="111")

    import logging
    logging.error("OK")

    return "OOOOL"
    return DefaultSuccessResponse()
