"""General API response schema."""

from typing import TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

DataT = TypeVar("DataT", bound=BaseModel)


class APIResponse[DataT: BaseModel](GenericModel):
    """Base schema for API responses."""

    success: bool = Field(..., description="Indicates if the request was successful")
    message: str = Field(..., description="Response message")
    data: DataT | None = Field(default=None, description="Response data, if any")
