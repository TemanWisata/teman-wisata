"""Module for Place Schema."""

from pydantic import UUID4, BaseModel, Field

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


class TopPlaceRating(BaseModel):
    """Schema for top place rating."""

    id: str | UUID4 = Field(
        description="Unique identifier for the place.",
    )
    place_id: int = Field(description="Unique identifier for the place in the database.")
    place_name: str = Field(description="Name of the place.")
    category: CategoryEnum = Field(description="Category of the place.")
    description: str | None = Field(default=None, description="Description of the place.")
    province: str = Field(default="Jakarta", description="Province where the place is located.")
    avg_rating: float = Field(description="Average rating of the place.")
    rating_count: int = Field(description="Number of ratings for the place.")
    rank: int | None = Field(
        default=None,
        description="Rank of the place in its province based on rating.",
    )


class TopPlaceByProvince(BaseModel):
    """Schema for top places by province."""

    province: str = Field(description="Province where the places are located.")
    data: list[TopPlaceRating] = Field(
        description="List of top places in the specified province.",
    )


class TopPlaceByCategory(BaseModel):
    """Schema for top places by category."""

    category: CategoryEnum = Field(description="Category of the places.")
    data: list[TopPlaceRating] = Field(
        description="List of top places in the specified category.",
    )
