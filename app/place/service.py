"""Module for Place API Service."""

from fastapi import HTTPException, status
from pydantic import TypeAdapter

from app.model import Place
from app.place.schema import PlaceFilter
from supabase import AsyncClient


class PlaceService:
    """Service class for handling Place-related operations."""

    @staticmethod
    async def get_all_places(supabase: AsyncClient, limit: int = 20, page: int = 1, query_filter: PlaceFilter | None = None) -> list[Place]:
        """Get all places."""
        offset = (page - 1) * limit
        query = supabase.from_("places").select("*")
        if query_filter:
            if query_filter.category:
                query = query.eq("category", query_filter.category.value)
            if query_filter.province:
                query = query.eq("province", query_filter.province)
            if query_filter.min_price is not None:
                query = query.gte("price", query_filter.min_price)
            if query_filter.max_price is not None:
                query = query.lte("price", query_filter.max_price)
            if query_filter.min_rating is not None:
                query = query.gte("rating", query_filter.min_rating)
            if query_filter.max_rating is not None:
                query = query.lte("rating", query_filter.max_rating)

        response = await query.range(offset, offset + limit - 1).execute()
        if response.data:
            return TypeAdapter(list[Place]).validate_python(response.data)
        return []

    @staticmethod
    async def get_place_by_id(supabase: AsyncClient, place_id: str) -> Place:
        """Get a place by its ID."""
        response = await supabase.from_("places").select("*").eq("id", place_id).single().execute()
        if response.data:
            return TypeAdapter(Place).validate_python(response.data)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
