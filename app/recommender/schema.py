"""Schema for recommender module."""

from pydantic import BaseModel, Field


class RecommenderRequest(BaseModel):
    """Request schema for recommender service."""

    k: int = Field(
        default=10,
        ge=1,
        description="Number of recommendations to return.",
    )
    filter_viewed: bool = Field(
        default=True,
        description="Whether to filter out items already viewed by the user.",
    )
    model_config = {
        "json_schema_extra": {
            "example": {
                "k": 10,
                "filter_viewed": True,
            },
        },
    }
