from api.v1 import bookmarks
from api.v1.endpoints import progress  # type: ignore
from fastapi import APIRouter

api_v1_router = APIRouter()
api_v1_router.include_router(progress.router, prefix="/progress", tags=["progress"])
api_v1_router.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])
