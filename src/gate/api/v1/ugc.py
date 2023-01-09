from http import HTTPStatus

from api.models import (
    MOVIE_ID,
    RATING_SCORE,
    USER_ID,
    BookmarkRecord,
    LikeRecord,
    RatingRecord,
    Response,
)
from fastapi import APIRouter, Depends
from service.mongo import (
    MongoService,
    get_bookmarks_service,
    get_likes_service,
    get_rating_service,
)

router: APIRouter = APIRouter()


@router.post(
    path="/{user_id}/bookmarks",
    response_model=Response,
)
async def create_bookmark(
    user_id: str = USER_ID,  # type: ignore
    movie_id: str = MOVIE_ID,  # type: ignore
    bookmarks_service: MongoService = Depends(get_bookmarks_service),
) -> Response:

    await bookmarks_service.create(
        user_id=user_id,
        movie_id=movie_id,
    )

    return Response(
        status=HTTPStatus.CREATED,
        message="Ok",
    )


@router.delete(
    path="/{user_id}/bookmarks",
    response_model=Response,
)
async def delete_bookmark(
    user_id: str = USER_ID,  # type: ignore
    movie_id: str = MOVIE_ID,  # type: ignore
    bookmarks_service: MongoService = Depends(get_bookmarks_service),
) -> Response:

    await bookmarks_service.delete(
        user_id=user_id,
        movie_id=movie_id,
    )

    return Response(
        status=HTTPStatus.CREATED,
        message="Ok",
    )


@router.get(
    path="/{user_id}/bookmarks",
    response_model=list[BookmarkRecord],
)
async def get_bookmarks(
    user_id: str = USER_ID,  # type: ignore
    bookmarks_service: MongoService = Depends(get_bookmarks_service),
) -> list[BookmarkRecord]:

    return await bookmarks_service.get(
        user_id=user_id,
    )


@router.post(
    path="/{user_id}/likes",
    response_model=Response,
)
async def create_likes(
    user_id: str = USER_ID,  # type: ignore
    movie_id: str = MOVIE_ID,  # type: ignore
    likes_service: MongoService = Depends(get_likes_service),
) -> Response:

    await likes_service.create(
        user_id=user_id,
        movie_id=movie_id,
    )

    return Response(
        status=HTTPStatus.CREATED,
        message="Ok",
    )


@router.delete(
    path="/{user_id}/likes",
    response_model=Response,
)
async def delete_likes(
    user_id: str = USER_ID,  # type: ignore
    movie_id: str = MOVIE_ID,  # type: ignore
    likes_service: MongoService = Depends(get_likes_service),
) -> Response:

    await likes_service.delete(
        user_id=user_id,
        movie_id=movie_id,
    )

    return Response(
        status=HTTPStatus.CREATED,
        message="Ok",
    )


@router.get(
    path="/{user_id}/likes",
    response_model=list[LikeRecord],
)
async def get_likes(
    user_id: str = USER_ID,  # type: ignore
    likes_service: MongoService = Depends(get_likes_service),
) -> list[LikeRecord]:

    return await likes_service.get(  # type: ignore
        user_id=user_id,
    )


@router.post(
    path="/{user_id}/ratings",
    response_model=Response,
)
async def create_ratings(
    user_id: str = USER_ID,  # type: ignore
    movie_id: str = MOVIE_ID,  # type: ignore
    rating: int = RATING_SCORE,  # type: ignore
    rating_service: MongoService = Depends(get_rating_service),
) -> Response:

    await rating_service.create(
        user_id=user_id,
        movie_id=movie_id,
        rating=rating,
    )

    return Response(
        status=HTTPStatus.CREATED,
        message="Ok",
    )


@router.delete(
    path="/{user_id}/ratings",
    response_model=Response,
)
async def delete_ratings(
    user_id: str = USER_ID,  # type: ignore
    movie_id: str = MOVIE_ID,  # type: ignore
    rating_service: MongoService = Depends(get_rating_service),
) -> Response:

    await rating_service.delete(
        user_id=user_id,
        movie_id=movie_id,
    )

    return Response(
        status=HTTPStatus.CREATED,
        message="Ok",
    )


@router.get(
    path="/{user_id}/ratings",
    response_model=list[RatingRecord],
)
async def get_ratings(
    user_id: str = USER_ID,  # type: ignore
    rating_service: MongoService = Depends(get_rating_service),
) -> list[RatingRecord]:

    return await rating_service.get(  # type: ignore
        user_id=user_id,
    )
