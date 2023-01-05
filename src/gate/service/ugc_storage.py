import abc
from functools import lru_cache
from typing import Optional

from bson import ObjectId
from models.mongo import Bookmarks
from motor.motor_asyncio import AsyncIOMotorDatabase
from motor.motor_tornado import MotorCursor
from pydantic import BaseModel
from pymongo import results, typings

from db.mongo.mng_db import db


class UGCService(abc.ABC):
    collection: AsyncIOMotorDatabase

    async def get(self, _id: str) -> Optional[typings._DocumentType]:
        """
        Method for retrieving entity by its identifier
        @param _id: entity identifier
        """
        return await self.collection.find_one({"_id": ObjectId(_id)})

    async def filter(self, filters: dict) -> MotorCursor:
        """
        Method for retrieving entity with filters
        @param filters: mongo filters
        """
        result = await self.collection.find(filters)

        return result

    async def insert(self, model: BaseModel) -> results.InsertOneResult:
        """
        Method for inserting entity
        @param model: data to insert
        """
        result = await self.collection.insert_one(model.dict())
        return result

    async def update(self, filters: dict, model: dict) -> results.UpdateResult:
        """
        Method for updating entity
        @param filters: mongo filters
        @param model: data to update
        """
        result = await self.collection.update_one(filters, {"$set": model})
        return result

    async def delete(self, filters: dict) -> results.DeleteResult:
        """
        Method for deletion entity with filters
        @param filters: mongo filters
        """
        result = await self.collection.delete_one(filters)
        return result


class BookmarkUGCService(UGCService):
    collection = db.bookmarks

    async def insert(
        self, model: Bookmarks
    ) -> results.UpdateResult | results.InsertOneResult:
        _id = str(model.obj_id)
        exists = await self.get(_id)
        if exists:
            return await self.update(
                {"_id": _id}, {"film_ids": exists.get("film_ids", []) + model.film_ids}
            )
        return await super(BookmarkUGCService, self).insert(model=model)

    async def delete(self, filters: dict) -> bool:
        exists = await self.filter({"user_id": filters["user_id"]})

        if exists:

            try:
                idx = exists["film_ids"].index(filters.get(filters.get("film_id")))
            except ValueError:
                return False

            exists["film_ids"].pop(idx)
            await self.update(filters, {"film_ids": exists["film_ids"]})
            return True

        return False


class RatingUGCService(UGCService):
    collection = db.ratings


class ReviewUGCService(UGCService):
    collection = db.reviews


class MovieUGCService(UGCService):
    collection = db.movies


@lru_cache
def get_movie_ugc_service() -> MovieUGCService:
    return MovieUGCService()


@lru_cache
def get_review_ugc_service() -> ReviewUGCService:
    return ReviewUGCService()


@lru_cache
def get_rating_ugc_service() -> RatingUGCService:
    return RatingUGCService()


@lru_cache
def get_bookmark_ugc_service() -> BookmarkUGCService:
    return BookmarkUGCService()
