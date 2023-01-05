import uuid
from uuid import UUID

from fastapi import APIRouter, Depends, responses
from models.mongo import Ratings
from service.ugc_storage import RatingUGCService, get_rating_ugc_service

router = APIRouter()


@router.get(path="/", response_model=Ratings)
async def get_rating(
    film_id: UUID,
    user_id: UUID,
    service: RatingUGCService = Depends(get_rating_ugc_service),
):
    """
    Endpoint for retrieving user's movie rating
    @param user_id: user identifier
    @param film_id: movie identifier
    @param service: rating service
    """
    result = await service.filter({"user_id": user_id, "film_id": film_id})

    if result:
        return responses.JSONResponse(status_code=200, content=result[0])

    return responses.Response(status_code=204)


@router.post(path="/")
async def post_rating(
    body: Ratings, service: RatingUGCService = Depends(get_rating_ugc_service)
):
    """
    Endpoint for posting rating
    @param service: rating service
    @param body: request body
    """
    await service.insert(body)

    return responses.JSONResponse(
        status_code=200, content={"msg": "rating added", "movie_id": str(body.film_id)}
    )


@router.put(path="/")
async def put_rating(
    body: Ratings, service: RatingUGCService = Depends(get_rating_ugc_service)
):
    """
    Endpoint for posting rating
    @param service: rating service
    @param body: request body
    """
    await service.update(
        filters=body.dict(exclude={"rating"}), model=body.dict(include={"rating"})
    )

    return responses.JSONResponse(
        status_code=200, content={"msg": "rating added", "movie_id": str(body.film_id)}
    )


@router.delete(path="/")
async def del_rating(
    film_id: uuid.UUID,
    user_id: uuid,
    service: RatingUGCService = Depends(get_rating_ugc_service),
):
    """
    Method for user's movie rating deletion
    @param film_id: movie identifier
    @param user_id: user identifier
    @param service: rating service
    """
    await service.delete({"user_id": user_id, "film_id": film_id})
    return responses.Response(status_code=202)
