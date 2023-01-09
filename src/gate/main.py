import logging
import os

import sentry_sdk
from aiokafka import AIOKafkaProducer  # type: ignore
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from sentry_sdk.integrations.fastapi import FastApiIntegration

from core.config import config
from db.kafka.kfk_producer import get_kafka_producer
from db.mongo import mng_db

logging.error("global")
logging.error(os.environ)


sentry_sdk.init(
    dsn=config.sentry.dsn, integrations=[FastApiIntegration(transaction_style="url")]
)

app = FastAPI(
    title=config.app_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup_event():
    """Startup routine"""
    logging.error("startup")
    logging.error(os.environ)

    kafka_producer: AIOKafkaProducer = get_kafka_producer()  # type: ignore
    await kafka_producer.start()

    logging.error("mongo start")

    mng_db.aio_mongo_client = AsyncIOMotorClient(
        host=config.mongo.host,
        port=config.mongo.port,
    )

    mng_db.aio_mongo_client_session = await mng_db.aio_mongo_client.start_session()

    logging.error("routing init")

    from api.v1.routes import api_v1_router  # type: ignore # noqa

    app.include_router(api_v1_router, prefix="/api/v1")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown routine"""
    kafka_producer: AIOKafkaProducer = get_kafka_producer()  # type: ignore
    await kafka_producer.stop()

    await mng_db.aio_mongo_client.end_session()
    await mng_db.aio_mongo_client.close
