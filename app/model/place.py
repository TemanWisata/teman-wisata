"""Model for Place Schema."""

from enum import Enum

from pydantic import UUID4, BaseModel, Field


class CategoryEnum(str, Enum):
    """Enum for place categories."""

    BUDAYA = "Budaya"
    TAMAN_HIBURAN = "Taman Hiburan"
    BAHARI = "Bahari"
    PUSAT_PERBELANJAAN = "Pusat Perbelanjaan"
    CAGAR_ALAM = "Cagar Alam"
    TEMPAT_IBADAH = "Tempat Ibadah"


class Place(BaseModel):
    """Model for Place."""

    id: str | UUID4 | None = Field(default=None, description="Unique identifier for the place")
    place_id: int = Field(description="Unique identifier for the place in the database, from dataset")
    place_name: str = Field(description="Name of the place, e.g., 'Museum Nasional', 'Taman Mini Indonesia Indah', etc.")
    description: str | None = Field(
        default=None,
        description="Description of the place, providing additional information about its significance or features.",
    )
    category: CategoryEnum = Field(default=CategoryEnum.BUDAYA, description="Category of the place, e.g., 'Budaya', 'Taman Hiburan', etc.")
    province: str = Field(default="Jakarta", description="Province where the place is located, e.g., 'Jakarta', 'Bali', etc.")
    price: float | None = Field(default=None, description="Price of the place, e.g., entry fee, ticket price, etc.")
    rating: float = Field(default=0.0, description="Rating of the place, e.g., average user rating out of 5.")
    time_minutes: float | None = Field(default=None, description="Estimated time to spend at the place, in minutes.")
    latitude: float | None = Field(
        default=None,
        description="Latitude coordinate of the place.",
    )
    longitude: float | None = Field(default=None, description="Longitude coordinate of the place.")
