"""Module for Recommender API."""

from fastapi import APIRouter

from app.infrastructure.di import SupabaseClientDependency
from app.place.service import PlaceService

router = APIRouter(
    prefix="/recommender",
    responses={404: {"description": "Not found"}},
)


@router.get("/user_ratings")
async def get_user_ratings(supabase_client: SupabaseClientDependency) -> dict | None:
    """Get user ratings DataFrame."""
    df = await PlaceService.get_all_user_place_ratings_df(supabase_client)  # noqa: F841
    return None
