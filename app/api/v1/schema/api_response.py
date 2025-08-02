"""General API response schema."""

from pydantic import BaseModel, Field


class APIResponse(BaseModel):
    """Base schema for API responses."""

    success: bool = Field(..., description="Indicates if the request was successful")
    message: str = Field(..., description="Response message")
    data: dict | None = Field(default=None, description="Response data, if any")
