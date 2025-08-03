"""General API response schema."""

from typing import TypeVar

from fastapi import status
from pydantic import BaseModel, Field

DataT = TypeVar("DataT", bound=BaseModel)


class APIResponse[DataT: BaseModel](BaseModel):
    """Base schema for API responses."""

    success: bool = Field(..., description="Indicates if the request was successful")
    http_status: int = Field(status.HTTP_200_OK, description="HTTP status code of the response")
    message: str = Field(..., description="Response message")
    data: DataT | None = Field(default=None, description="Response data, if any")
