import sentry_sdk
from aiokafka import AIOKafkaProducer  # type: ignore
from api.v1.routes import api_v1_router  # type: ignore
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.fastapi import FastApiIntegration

from core.config import config
from db.kafka.kfk_producer import get_kafka_producer

sentry_sdk.init(
    dsn=config.sentry.dsn, integrations=[FastApiIntegration(transaction_style="url")]
)

app = FastAPI(
    title=config.app_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(api_v1_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Startup routine"""
    kafka_producer: AIOKafkaProducer = get_kafka_producer()
    await kafka_producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown routine"""
    kafka_producer: AIOKafkaProducer = get_kafka_producer()
    await kafka_producer.stop()
