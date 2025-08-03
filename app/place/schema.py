"""Module for Place Schema."""

from pydantic import BaseModel, Field

from app.model import CategoryEnum


class PlaceFilter(BaseModel):
    """Schema for filtering places."""

    category: CategoryEnum | None = Field(
        default=None,
        description="Category of the place, e.g., 'Budaya', 'Taman Hiburan', etc.",
    )
    min_price: float | None = Field(
        default=None,
        description="Minimum price of the place.",
    )
    max_price: float | None = Field(
        default=None,
        description="Maximum price of the place.",
    )
    min_rating: float | None = Field(
        default=None,
        description="Minimum rating of the place.",
    )
    max_rating: float | None = Field(
        default=None,
        description="Maximum rating of the place.",
    )

    province: str | None = Field(
        default=None,
        description="Province where the place is located.",
    )
