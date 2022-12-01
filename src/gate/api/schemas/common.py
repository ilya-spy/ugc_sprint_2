from pydantic import Field

from api.schemas.base import BaseAPISchema


class DefaultSuccessResponse(BaseAPISchema):
    """Общий успешный ответ"""

    status: str = Field("success")
