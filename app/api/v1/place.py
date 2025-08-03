"""Route for Place API."""

from fastapi import APIRouter

router = APIRouter(prefix="/place", tags=["place"])


@router.get("/")
async def get_places() -> dict:
    """Get all places."""
    return {"message": "List of places"}


@router.get("/{place_id}")
async def get_place(place_id: int) -> dict:
    """Get a specific place by ID."""
    return {"message": f"Details of place {place_id}"}


@router.get("/top")
async def top_places() -> dict:
    """Get top places."""
    return {"message": "List of top places"}


@router.get("/top/category")
async def top_places_by_category(category: str) -> dict:
    """Get top places by category."""
    return {"message": f"List of top places in category {category}"}


@router.post("/{place_id}/rate")
async def rate_place(place_id: int, rating: float) -> dict:
    """Rate a place."""
    return {"message": f"Rated place {place_id} with rating {rating}"}
