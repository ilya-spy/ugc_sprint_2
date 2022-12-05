from api.schemas.common import DefaultSuccessResponse
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import ValidationError
from service.auth_api import AuthApiService, get_auth_api_service
from service.event_storage import EventStorageService, get_event_storage_service

router = APIRouter()


@router.post(path="/", response_model=DefaultSuccessResponse)
async def save(
    request: Request,
    event_storage_service: EventStorageService = Depends(get_event_storage_service),
    auth_api_service: AuthApiService = Depends(get_auth_api_service),
) -> DefaultSuccessResponse:
    try:
        user = await auth_api_service.get_user_info(headers=dict(request.headers))
    except (TypeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    await event_storage_service.send("tp_1", {"seconds": 1, "user_id": str(user.id)})

    return DefaultSuccessResponse()
