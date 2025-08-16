"""Module for Place Schema."""

from pydantic import UUID4, BaseModel, Field

from app.model import CategoryEnum, Place


class PlaceFilter(BaseModel):
    """Schema for filtering places."""

    category: CategoryEnum | None = Field(
        description="Category of the place, e.g., 'Budaya', 'Taman Hiburan', etc.",
    )
    min_price: float | None = Field(
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
        description="Province where the place is located.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "category": None,
                "min_price": None,
                "max_price": None,
                "min_rating": None,
                "max_rating": None,
                "province": None,
            },
        },
    }


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


class ResponseTopPlaceRating(BaseModel):
    """Schema for response of top place rating."""

    places: list[TopPlaceRating] | list = Field(
        default=[],
        description="List of top places with their ratings.",
    )


class RecommendedPlace(BaseModel):
    """Schema for recommended place."""

    data: list[Place | None] = Field(
        description="List of recommended places.",
    )


class TopPlaceByProvince(BaseModel):
    """Schema for top places by province."""

    province: str = Field(description="Province where the places are located.")
    places: list[TopPlaceRating] = Field(
        description="List of top places in the specified province.",
    )


class ResponseTopPlaceByProvince(BaseModel):
    """Schema for response of top places by province."""

    data: list[TopPlaceByProvince] | list = Field(
        default=[],
        description="List of top places grouped by province.",
    )


class TopPlaceByCategory(BaseModel):
    """Schema for top places by category."""

    category: CategoryEnum = Field(description="Category of the places.")
    places: list[TopPlaceRating] = Field(
        description="List of top places in the specified category.",
    )


class ResponseTopPlaceByCategory(BaseModel):
    """Schema for response of top places by category."""

    data: list[TopPlaceByCategory] | list = Field(
        default=[],
        description="List of top places grouped by category.",
    )


class AllPlaceRequest(BaseModel):
    """Schema for all places request."""

    query_filter: PlaceFilter | None = Field(
        default=None,
        description="Filter criteria for fetching places.",
    )
    page: int = Field(
        default=1,
        ge=1,
        description="Page number for pagination.",
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of places to return per page.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "query_filter": None,
                "page": 1,
                "limit": 10,
            },
        },
    }


class PaginationResponse(BaseModel):
    """Schema for pagination response."""

    total: int = Field(description="Total number of places available.")
    page: int = Field(description="Current page number.")
    has_next: bool = Field(
        description="Indicates if there is a next page.",
    )
    has_prev: bool = Field(
        description="Indicates if there is a previous page.",
    )
    next_page: int | None = Field(
        default=None,
        description="Next page number if available.",
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of places to return per page.",
    )


class ResponsePlace(BaseModel):
    """Schema for place response."""

    places: list[Place] = Field(
        description="Data of the place.",
    )
    pagination: PaginationResponse = Field(
        description="Pagination information for the response.",
    )


class UserRating(BaseModel):
    """Schema for user rating of a place."""

    user_id: int = Field(description="Unique identifier for the user.")
    place_id: int = Field(description="Unique identifier for the place.")
    rating: float = Field(
        ge=0.0,
        le=5.0,
        description="Rating given by the user, between 0 and 5.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "place_id": 1,
                "rating": 4.5,
            },
        },
    }


class UserRatingRequest(BaseModel):
    """Schema for user rating request."""

    place_id: int = Field(description="Unique identifier for the place.")
    rating: float = Field(
        ge=0.0,
        le=5.0,
        description="Rating given by the user, between 0 and 5.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "rating": 4.5,
            },
        },
    }
