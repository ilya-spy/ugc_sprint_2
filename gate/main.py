import asyncio

from aiokafka import AIOKafkaProducer
from api.v1.routes import api_v1_router
from core.config import config
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from db import kafka

app = FastAPI(
    title=config.app_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(api_v1_router, prefix="/api/v1")

loop = asyncio.get_event_loop()
kafka.producer = AIOKafkaProducer(
    loop=loop, client_id=config.app_name, bootstrap_servers=config.kafka.instance
)


@app.on_event("startup")
async def startup_event():
    await kafka.producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka.producer.stop()
