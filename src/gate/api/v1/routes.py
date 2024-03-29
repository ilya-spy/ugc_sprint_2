from api.v1 import ugc  # type: ignore
from api.v1.endpoints import progress  # type: ignore
from fastapi import APIRouter

api_v1_router = APIRouter()

api_v1_router.include_router(progress.router, prefix="/progress", tags=["progress"])
api_v1_router.include_router(ugc.router, prefix="/feedback", tags=["movie-related"])
