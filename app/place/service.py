"""Module for Place API Service."""

from collections import defaultdict  # noqa: I001
from typing import Any
from fastapi import HTTPException, status
from pydantic import TypeAdapter, ValidationError
from supabase import AsyncClient
from postgrest.base_request_builder import BaseFilterRequestBuilder
from postgrest.types import CountMethod
from app.model import Place
from app.place.schema import (
    PlaceFilter,
    TopPlaceByCategory,
    TopPlaceByProvince,
    TopPlaceRating,
    PaginationResponse,
    ResponsePlace,
    ResponseTopPlaceByCategory,
    ResponseTopPlaceByProvince,
    ResponseTopPlaceRating,
    UserRating,
)


class PlaceService:
    """Service class for handling Place-related operations."""

    @classmethod
    async def get_all_places(cls, supabase: AsyncClient, limit: int = 20, page: int = 1, query_filter: PlaceFilter | None = None) -> ResponsePlace:
        """Get all places."""
        try:
            offset = (page - 1) * limit
            base_query = supabase.from_("place").select("*")
            filter_query = cls._apply_filters(base_query, query_filter)
            count_query = cls._apply_filters(supabase.from_("place").select("*", count=CountMethod.exact), query_filter)
            count_response = await count_query.execute()
            total_records = count_response.count or 0
            total_page = (total_records + limit - 1) // limit
            response = await filter_query.range(offset, offset + limit - 1).execute()

            places = TypeAdapter(list[Place]).validate_python(response.data) if response.data else []

            return ResponsePlace(places=places, pagination=PaginationResponse(total=total_page, has_next=len(places) == limit, has_prev=page > 1, page=page, limit=limit))
        except HTTPException:
            raise
        except ValidationError as ve:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Validation error", "errors": ve.errors()})  # noqa: B904
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))  # noqa: B904

    @classmethod
    def _apply_filters(cls, query: BaseFilterRequestBuilder, query_filter: PlaceFilter | None) -> Any:  # noqa: ANN401
        """Apply filters to query in a centralized way."""
        try:
            if not query_filter:
                return query

            filter_mappings = [
                (query_filter.category, "category", "eq", query_filter.category.value if query_filter.category else None),
                (query_filter.province, "province", "eq", query_filter.province),
                (query_filter.min_price, "price", "gte", query_filter.min_price),
                (query_filter.max_price, "price", "lte", query_filter.max_price),
                (query_filter.min_rating, "rating", "gte", query_filter.min_rating),
                (query_filter.max_rating, "rating", "lte", query_filter.max_rating),
            ]

            for condition, field, operator, value in filter_mappings:
                if condition is not None:
                    if operator == "eq":
                        query = query.eq(field, value)
                    elif operator == "gte":
                        query = query.gte(field, value)
                    elif operator == "lte":
                        query = query.lte(field, value)

        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid filter: {e!s}")  # noqa: B904
        return query

    @staticmethod
    async def get_place_by_id(supabase: AsyncClient, place_id: str) -> Place:
        """Get a place by its ID."""
        try:
            response = await supabase.from_("place").select("*").eq("id", place_id).single().execute()
            if response.data:
                return TypeAdapter(Place).validate_python(response.data)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")  # noqa: TRY301
        except ValidationError as ve:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Validation error", "errors": ve.errors()})  # noqa: B904
        except HTTPException:
            raise
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))  # noqa: B904

    @staticmethod
    async def get_top_places(supabase: AsyncClient, limit: int = 10) -> ResponseTopPlaceRating:
        """Get top places based on rating."""
        try:
            response = await supabase.rpc("get_top_places_rating", {"limit_param": limit}).execute()

            if response.data:
                data = TypeAdapter(list[TopPlaceRating]).validate_python(response.data)
                return ResponseTopPlaceRating(places=data)
        except ValidationError as ve:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Validation error", "errors": ve.errors()})  # noqa: B904
        except HTTPException:
            raise
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))  # noqa: B904
        return ResponseTopPlaceRating()

    @staticmethod
    async def get_top_places_by_province(supabase: AsyncClient, limit: int = 10) -> ResponseTopPlaceByProvince:
        """Get top places based on rating."""
        try:
            response = await supabase.rpc("get_top_places_by_province", {"limit_param": limit}).execute()
            grouped = defaultdict(list)
            if response.data:
                for item in response.data:
                    grouped[item["province"]].append(item)
                result = [{"province": province, "places": grouped_data} for province, grouped_data in grouped.items()]

                data = TypeAdapter(list[TopPlaceByProvince]).validate_python(result)

                return ResponseTopPlaceByProvince(data=data)

            return ResponseTopPlaceByProvince()
        except ValidationError as ve:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Validation error", "errors": ve.errors()})  # noqa: B904
        except HTTPException:
            raise
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))  # noqa: B904

    @staticmethod
    async def get_top_places_by_category(supabase: AsyncClient, limit: int = 10) -> ResponseTopPlaceByCategory:
        """Get top places based on rating."""
        try:
            response = await supabase.rpc("get_top_places_by_category", {"limit_param": limit}).execute()
            grouped = defaultdict(list)
            if response.data:
                for item in response.data:
                    grouped[item["category"]].append(item)
                result = [{"category": category, "places": grouped_data} for category, grouped_data in grouped.items()]

                data = TypeAdapter(list[TopPlaceByCategory]).validate_python(result)

                return ResponseTopPlaceByCategory(data=data)
            return ResponseTopPlaceByCategory()
        except ValidationError as ve:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Validation error", "errors": ve.errors()})  # noqa: B904
        except HTTPException:
            raise
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))  # noqa: B904

    @staticmethod
    async def upsert_place_rating(supabase: AsyncClient, user_rating: UserRating) -> None:
        """Upsert place rating for a user."""
        try:
            await supabase.from_("user_place_rating").upsert({"user_id": user_rating.user_id, "place_id": user_rating.place_id, "rating": user_rating.rating}).execute()
        except ValidationError as ve:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "Validation error", "errors": ve.errors()})  # noqa: B904
        except HTTPException:
            raise
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))  # noqa: B904
