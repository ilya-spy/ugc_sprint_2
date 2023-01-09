from abc import abstractmethod
from typing import Optional, Type, Union
from uuid import UUID

from api.models import BookmarkRecord, LikeRecord, RatingRecord  # type: ignore
from async_lru import alru_cache  # type: ignore
from motor.motor_asyncio import AsyncIOMotorClientSession  # type: ignore # noqa
from motor.motor_asyncio import AsyncIOMotorCollection  # noqa
from motor.motor_asyncio import AsyncIOMotorCursor  # noqa
from motor.motor_asyncio import AsyncIOMotorDatabase  # noqa

from db.mongo.mng_db import get_mongo_client_session, get_mongo_db

_RecordTypes = Union[BookmarkRecord, LikeRecord, RatingRecord]


class MongoService:
    def __init__(
        self,
        mongo_db: AsyncIOMotorDatabase,
        mongo_session: AsyncIOMotorClientSession,
    ):
        self.mongo_db: AsyncIOMotorDatabase = mongo_db
        self.collection: AsyncIOMotorCollection = self.mongo_db[self.collection_name]
        self.mongo_session: AsyncIOMotorClientSession = mongo_session

    @property
    @abstractmethod
    def collection_name(self) -> str:
        ...

    @property
    @abstractmethod
    def record_model(self) -> Type[_RecordTypes]:
        ...

    async def get(
        self,
        *,
        user_id: Union[str, UUID],
        movie_id: Optional[Union[str, UUID]] = None,
    ) -> list[_RecordTypes]:

        filter_: dict = {"user_id": user_id}

        if movie_id is not None:
            filter_.update({"movie_id": movie_id})

        records: AsyncIOMotorCursor = self.collection.find(
            filter_,
            session=self.mongo_session,
        )

        return [self.record_model(**record) async for record in records]

    async def delete(
        self,
        *,
        user_id: Union[str, UUID],
        movie_id: Union[str, UUID],
    ) -> None:

        await self.collection.find_one_and_delete(
            {
                "user_id": user_id,
                "movie_id": movie_id,
            },
            session=self.mongo_session,
        )

    async def create(
        self,
        *,
        user_id: Union[str, UUID],
        movie_id: Union[str, UUID],
        **kwargs,
    ) -> None:

        existing_records = await self.get(
            user_id=user_id,
            movie_id=movie_id,
        )

        if existing_records:
            return

        await self.collection.insert_one(
            {
                "user_id": user_id,
                "movie_id": movie_id,
                **kwargs,
            },
            session=self.mongo_session,
        )


class BookmarksService(MongoService):
    @property
    def collection_name(self) -> str:
        return "bookmarks_collection"

    @property
    def record_model(self) -> Type[_RecordTypes]:
        return BookmarkRecord


class RatingService(MongoService):
    @property
    def collection_name(self) -> str:
        return "rating_collection"

    @property
    def record_model(self) -> Type[_RecordTypes]:
        return RatingRecord


class LikesService(MongoService):
    @property
    def collection_name(self) -> str:
        return "likes_collection"

    @property
    def record_model(self) -> Type[_RecordTypes]:
        return LikeRecord


@alru_cache
async def get_bookmarks_service() -> MongoService:
    return BookmarksService(await get_mongo_db(), await get_mongo_client_session())


@alru_cache
async def get_rating_service() -> RatingService:
    return RatingService(await get_mongo_db(), await get_mongo_client_session())


@alru_cache
async def get_likes_service() -> LikesService:
    return LikesService(await get_mongo_db(), await get_mongo_client_session())
