from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.routes import api_v1_router
from core import config

app = FastAPI(
    title=config.APP_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(api_v1_router, prefix="/api/v1")
