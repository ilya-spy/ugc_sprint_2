from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClientSession  # noqa
from motor.motor_asyncio import AsyncIOMotorDatabase  # noqa
from motor.motor_asyncio import AsyncIOMotorClient

aio_mongo_client: Optional[AsyncIOMotorClient] = None
aio_mongo_client_session: Optional[AsyncIOMotorClientSession] = None


async def get_mongo_db() -> AsyncIOMotorDatabase:
    return aio_mongo_client.get_database("movie_feedback")  # type: ignore


async def get_mongo_client_session() -> AsyncIOMotorClientSession:
    return aio_mongo_client_session
