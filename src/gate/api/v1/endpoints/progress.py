from fastapi import APIRouter, Depends

from api.schemas.common import DefaultSuccessResponse
from service.event_storage import EventStorageService, get_event_storage_service

router = APIRouter()


@router.post(path="/", response_model=DefaultSuccessResponse)
async def save(
    event_storage_service: EventStorageService = Depends(get_event_storage_service)
) -> DefaultSuccessResponse:
    await event_storage_service.send("tp_1", {"a": 1})

    return DefaultSuccessResponse()
