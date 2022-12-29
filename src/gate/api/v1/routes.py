from api.v1.endpoints import progress  # type: ignore
from fastapi import APIRouter

api_v1_router = APIRouter()
api_v1_router.include_router(progress.router, prefix="/progress", tags=["progress"])
