"""Route for Place API."""

from fastapi import APIRouter, HTTPException, Request

from app.api.v1.schema.api_response import APIResponse
from app.infrastructure.di import SupabaseClientDependency
from app.model import Place
from app.place import AllPlaceRequest, PlaceResponse, PlaceService

router = APIRouter(prefix="/place")


@router.post("/")
async def get_places(request: Request, supabase_client: SupabaseClientDependency, api_request: AllPlaceRequest) -> APIResponse[PlaceResponse]:  # noqa: ARG001
    """Get all places."""
    try:
        result = await PlaceService.get_all_places(supabase_client, limit=api_request.limit, page=api_request.page, query_filter=api_request.query_filter)
        return APIResponse(success=True, http_status=200, message="Places retrieved successfully", data=result)
    except HTTPException as e:
        return APIResponse(success=False, http_status=e.status_code, message=str(e.detail), data=None)
    except Exception as e:  # noqa: BLE001
        return APIResponse(success=False, http_status=500, message=f"An unexpected error occurred: {e!s}", data=None)


@router.get("/{uuid_of_place}")
async def get_place(supabase_client: SupabaseClientDependency, uuid_of_place: str) -> APIResponse[Place]:
    """Get a specific place by ID."""
    if not uuid_of_place or uuid_of_place == "{uuid_of_place}":
        return APIResponse(success=False, http_status=400, message="UUID of place is required", data=None)
    try:
        place = await PlaceService.get_place_by_id(supabase_client, uuid_of_place)
        return APIResponse(success=True, http_status=200, message="Place retrieved successfully", data=place)
    except HTTPException as e:
        return APIResponse(success=False, http_status=e.status_code, message=str(e.detail), data=None)
    except Exception as e:  # noqa: BLE001
        return APIResponse(success=False, http_status=500, message=f"An unexpected error occurred: {e!s}", data=None)


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
