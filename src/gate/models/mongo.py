from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel, Field


class BaseCollectionMixin(BaseModel):
    obj_id: ObjectId


class UserRelatedMixin(BaseModel):
    user_id: UUID


class MovieRelatedMixin(BaseModel):
    film_id: UUID


class Ratings(BaseCollectionMixin, UserRelatedMixin, MovieRelatedMixin):
    rating: int = Field(ge=0, le=10)


class Bookmarks(BaseCollectionMixin, UserRelatedMixin):
    film_ids: list[UUID]


class Reviews(BaseCollectionMixin, UserRelatedMixin, MovieRelatedMixin):
    review: str


class Movies(BaseCollectionMixin):
    film_id: UUID
    reviews: list[ObjectId]
    ratings: list[ObjectId]
    avg_rating: float | int = Field(ge=0, le=10)
