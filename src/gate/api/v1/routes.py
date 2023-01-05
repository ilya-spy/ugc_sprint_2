from api.v1 import bookmarks, ratings
from api.v1.endpoints import progress  # type: ignore
from fastapi import APIRouter

api_v1_router = APIRouter()
api_v1_router.include_router(progress.router, prefix="/progress", tags=["progress"])
api_v1_router.include_router(bookmarks.router, prefix="/bookmark", tags=["bookmarks"])
api_v1_router.include_router(ratings.router, prefix="/rating", tags=["ratings"])
