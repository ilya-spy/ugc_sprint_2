from typing import Optional

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from core.config import config

client: Optional[AsyncIOMotorClient] = None
db: Optional[AsyncIOMotorDatabase] = None


def mongo_init():
    global client, db
    client = AsyncIOMotorClient(config.mongo.host, config.mongo.port)

    # DB initialization
    db = client.movie_feedback

    # Collections initialization
    movies = db.movies
    ratings = db.ratings
    bookmarks = db.bookmarks
    reviews = db.reviews

    # Additional settings for ratings collection
    ratings.create_index(
        [("user_id", pymongo.ASCENDING), ("film_id", pymongo.ASCENDING)], unique=True
    )

    # Additional settings for bookmarks collection
    bookmarks.create_index(
        [
            ("user_id", pymongo.ASCENDING),
        ],
        unique=True,
    )

    # Additional settings for review collection
    reviews.create_index(
        [("user_id", pymongo.ASCENDING), ("film_id", pymongo.ASCENDING)], unique=True
    )

    # Additional settings for review collection
    movies.create_index([("film_id", pymongo.ASCENDING)], unique=True)
