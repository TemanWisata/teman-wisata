"""Module for Place API Service."""

from collections import defaultdict  # noqa: I001

from fastapi import HTTPException, status
from pydantic import TypeAdapter
from supabase import AsyncClient

from app.core.utils import Utils
from app.model import Place
from app.place.schema import PlaceFilter, TopPlaceByCategory, TopPlaceByProvince, TopPlaceRating


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

    @staticmethod
    async def get_top_places(supabase: AsyncClient, limit: int = 10) -> list[TopPlaceRating]:
        """Get top places based on rating."""
        query = Utils.load_sql_file("./app/place/query/top_place_rating.sql").format(limit=limit)
        if not query:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="SQL query not found")

        response = await supabase.rpc("execute_sql", {"sql": query}).execute()

        if response.data:
            return TypeAdapter(list[TopPlaceRating]).validate_python(response.data)
        return []

    @staticmethod
    async def get_top_places_by_province(supabase: AsyncClient, limit: int = 10) -> list[TopPlaceByProvince]:
        """Get top places based on rating."""
        query = Utils.load_sql_file("./app/place/query/top_place_by_province.sql").format(limit=limit)
        if not query:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="SQL query not found")

        response = await supabase.rpc("execute_sql", {"sql": query}).execute()
        grouped = defaultdict(list)
        if response.data:
            for item in response.data:
                grouped[item["province"]].append(item)
            result = [{"province": province, "data": grouped_data} for province, grouped_data in grouped.items()]
            return TypeAdapter(list[TopPlaceByProvince]).validate_python(result)
        return []

    @staticmethod
    async def get_top_places_by_category(supabase: AsyncClient, limit: int = 10) -> list[TopPlaceByCategory]:
        """Get top places based on rating."""
        query = Utils.load_sql_file("./app/place/query/top_place_by_category.sql").format(limit=limit)
        if not query:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="SQL query not found")

        response = await supabase.rpc("execute_sql", {"sql": query}).execute()
        grouped = defaultdict(list)
        if response.data:
            for item in response.data:
                grouped[item["category"]].append(item)
            result = [{"category": category, "data": grouped_data} for category, grouped_data in grouped.items()]
            return TypeAdapter(list[TopPlaceByCategory]).validate_python(result)
        return []

    @staticmethod
    async def upsert_place_rating(supabase: AsyncClient, user_id: str, place_id: int, rating: float) -> None:
        """Upsert place rating for a user."""
        await supabase.from_("user_place_rating").upsert({"user_id": user_id, "place_id": place_id, "rating": rating}).execute()
