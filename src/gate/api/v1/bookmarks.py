from uuid import UUID

from fastapi import APIRouter, Depends, responses
from models.mongo import Bookmarks
from service.ugc_storage import BookmarkUGCService, get_bookmark_ugc_service

router = APIRouter()


@router.get(path="/")
async def get_bm(
    user_id: UUID, bm_service: BookmarkUGCService = Depends(get_bookmark_ugc_service)
):
    """
    Endpoint for retrieving user's bookmarks
    @param bm_service: bookmark service
    @param user_id: user identifier
    """
    q = await bm_service.filter({"user_id": user_id})
    result = q.to_list()

    if result:
        return responses.JSONResponse(status_code=200, content=result[0])

    return responses.Response(status_code=204)


@router.post(path="/")
async def post_bm(
    body: Bookmarks, bm_service: BookmarkUGCService = Depends(get_bookmark_ugc_service)
):
    """
    Endpoint for adding user's bookmark
    @param bm_service: bookmark service
    @param user_id: user identifier
    @param body: request body
    """
    await bm_service.insert(body)
    return responses.JSONResponse(
        status_code=201, content={"msg": "bookmark inserted", "bm_id": body.film_ids}
    )


@router.delete(path="/")
async def delete_bm(
    user_id: UUID,
    film_id: UUID,
    bm_service: BookmarkUGCService = Depends(get_bookmark_ugc_service),
):
    """
    Endpoint for deletion of user's bookmark
    @param bm_service: bookmark service
    @param user_id: user identifier
    @param film_id: film identifier
    """
    result = await bm_service.delete({"user_id": user_id, "film_id": film_id})

    if result:
        return responses.Response(status_code=202)

    return responses.Response(status_code=204)
