from fastapi import APIRouter, Depends, Request, HTTPException, status
from pydantic import ValidationError

from models.event import InputEvent, WatchProgressEvent
from api.schemas.common import DefaultSuccessResponse
from service.event_storage import EventStorageService, get_event_storage_service
from service.auth_api import AuthApiService, get_auth_api_service

router = APIRouter()


@router.post(path="/", response_model=DefaultSuccessResponse)
async def save(
    request: Request,
    event: InputEvent,
    event_storage_service: EventStorageService = Depends(get_event_storage_service),
    auth_api_service: AuthApiService = Depends(get_auth_api_service),
) -> DefaultSuccessResponse:
    try:
        user = await auth_api_service.get_user_info(headers=dict(request.headers))
    except (TypeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    model = WatchProgressEvent(
        **(event.dict()),
        user_id=user.id,
    )

    await event_storage_service.send(
        topic_name="watching_progress",
        model=model.convert_to_kafka_event(),
    )

    return DefaultSuccessResponse()
