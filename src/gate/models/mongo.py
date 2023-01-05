from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel, Field


class UserRelatedMixin(BaseModel):
    user_id: UUID


class MovieRelatedMixin(BaseModel):
    film_id: UUID


class Ratings(UserRelatedMixin, MovieRelatedMixin):
    rating: int = Field(ge=0, le=10)


class Bookmarks(UserRelatedMixin):
    film_ids: list[UUID]


class Reviews(UserRelatedMixin, MovieRelatedMixin):
    review: str


class Movies:
    film_id: UUID
    reviews: list[ObjectId]
    ratings: list[ObjectId]
    avg_rating: float | int = Field(ge=0, le=10)
