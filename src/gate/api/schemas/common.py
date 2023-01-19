from api.schemas.base import BaseAPISchema  # type: ignore
from pydantic import Field


class DefaultSuccessResponse(BaseAPISchema):
    """Общий успешный ответ"""

    status: str = Field("success")
