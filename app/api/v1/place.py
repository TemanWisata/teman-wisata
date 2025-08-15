"""Route for Place API."""

from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError

from app.api.v1.schema.api_response import APIResponse
from app.auth import verify_bearer_token
from app.infrastructure.di import SupabaseClientDependency
from app.model import Place
from app.place import AllPlaceRequest, PlaceService, ResponsePlace, ResponseTopPlaceByCategory, ResponseTopPlaceByProvince, ResponseTopPlaceRating, UserRating, UserRatingRequest

router = APIRouter(prefix="/place")


@router.post("/")
async def get_places(request: Request, supabase_client: SupabaseClientDependency, api_request: AllPlaceRequest, verify_user: verify_bearer_token) -> APIResponse[ResponsePlace]:  # noqa: ARG001
    """Get all places."""
    try:
        result = await PlaceService.get_all_places(supabase_client, limit=api_request.limit, page=api_request.page, query_filter=api_request.query_filter)
        return APIResponse(success=True, http_status=200, message="Places retrieved successfully", data=result)
    except ValidationError as e:
        return APIResponse(success=False, http_status=400, message=f"Validation error: {e.errors()}", data=None)
    except HTTPException as e:
        return APIResponse(success=False, http_status=e.status_code, message=str(e.detail), data=None)
    except Exception as e:  # noqa: BLE001
        return APIResponse(success=False, http_status=500, message=f"An unexpected error occurred: {e!s}", data=None)


@router.get("/{uuid_of_place}/")
async def get_place(supabase_client: SupabaseClientDependency, uuid_of_place: str, verify_user: verify_bearer_token) -> APIResponse[Place]:  # noqa: ARG001
    """Get a specific place by ID."""
    if not uuid_of_place or uuid_of_place == "{uuid_of_place}":
        return APIResponse(success=False, http_status=400, message="UUID of place is required", data=None)
    try:
        place = await PlaceService.get_place_by_id(supabase_client, uuid_of_place)
        return APIResponse(success=True, http_status=200, message="Place retrieved successfully", data=place)
    except ValidationError as e:
        return APIResponse(success=False, http_status=400, message=f"Validation error: {e.errors()}", data=None)
    except HTTPException as e:
        return APIResponse(success=False, http_status=e.status_code, message=str(e.detail), data=None)
    except Exception as e:  # noqa: BLE001
        return APIResponse(success=False, http_status=500, message=f"An unexpected error occurred: {e!s}", data=None)


@router.get("/top")
async def top_places(supabase_client: SupabaseClientDependency, verify_user: verify_bearer_token) -> APIResponse[ResponseTopPlaceRating]:  # noqa: ARG001
    """Get top places."""
    try:
        result = await PlaceService.get_top_places(supabase_client, limit=10)
        return APIResponse(success=True, http_status=200, message="Top places retrieved successfully", data=result)
    except ValidationError as e:
        return APIResponse(success=False, http_status=400, message=f"Validation error: {e.errors()}", data=None)
    except HTTPException as e:
        return APIResponse(success=False, http_status=e.status_code, message=str(e.detail), data=None)
    except Exception as e:  # noqa: BLE001
        return APIResponse(success=False, http_status=500, message=f"An unexpected error occurred: {e!s}", data=None)


@router.get("/top/category")
async def top_places_by_category(supabase_client: SupabaseClientDependency, verify_user: verify_bearer_token) -> APIResponse[ResponseTopPlaceByCategory]:  # noqa: ARG001
    """Get top places by category."""
    try:
        result = await PlaceService.get_top_places_by_category(supabase_client, limit=10)
        return APIResponse(success=True, http_status=200, message="Top places by category retrieved successfully", data=result)
    except ValidationError as e:
        return APIResponse(success=False, http_status=400, message=f"Validation error: {e.errors()}", data=None)

    except HTTPException as e:
        return APIResponse(success=False, http_status=e.status_code, message=str(e.detail), data=None)
    except Exception as e:  # noqa: BLE001
        return APIResponse(success=False, http_status=500, message=f"An unexpected error occurred: {e!s}", data=None)


@router.get("/top/province")
async def top_places_by_province(supabase_client: SupabaseClientDependency, verify_user: verify_bearer_token) -> APIResponse[ResponseTopPlaceByProvince]:  # noqa: ARG001
    """Get top places by province."""
    try:
        result = await PlaceService.get_top_places_by_province(supabase_client, limit=10)
        return APIResponse(success=True, http_status=200, message="Top places by province retrieved successfully", data=result)
    except ValidationError as e:
        return APIResponse(success=False, http_status=400, message=f"Validation error: {e.errors()}", data=None)
    except HTTPException as e:
        return APIResponse(success=False, http_status=e.status_code, message=str(e.detail), data=None)
    except Exception as e:  # noqa: BLE001
        return APIResponse(success=False, http_status=500, message=f"An unexpected error occurred: {e!s}", data=None)


@router.post("/rate")
async def rate_place(supabase_client: SupabaseClientDependency, rating_request: UserRatingRequest, verify_user: verify_bearer_token) -> APIResponse[UserRating]:
    """Rate a place."""
    try:
        request_rating = UserRating(
            user_id=verify_user.user_id,
            place_id=rating_request.place_id,
            rating=rating_request.rating,
        )
        await PlaceService.upsert_place_rating(supabase_client, request_rating)
        return APIResponse(success=True, http_status=200, message="Rating submitted successfully", data=request_rating)
    except ValidationError as e:
        return APIResponse(success=False, http_status=400, message=f"Validation error: {e.errors()}", data=None)
    except HTTPException as e:
        return APIResponse(success=False, http_status=e.status_code, message=str(e.detail), data=None)
    except Exception as e:  # noqa: BLE001
        return APIResponse(success=False, http_status=500, message=f"An unexpected error occurred: {e!s}", data=None)


@router.get("/rate/{place_id}")
async def get_user_rating(supabase_client: SupabaseClientDependency, place_id: int, verify_user: verify_bearer_token) -> APIResponse[UserRating]:
    """Get user rating for a place."""
    try:
        result = await PlaceService.get_user_place_rating(supabase_client, verify_user.user_id, place_id)
        return APIResponse(success=True, http_status=200, message="User rating retrieved successfully", data=result)
    except ValidationError as e:
        return APIResponse(success=False, http_status=400, message=f"Validation error: {e.errors()}", data=None)
    except HTTPException as e:
        return APIResponse(success=False, http_status=e.status_code, message=str(e.detail), data=None)
    except Exception as e:  # noqa: BLE001
        return APIResponse(success=False, http_status=500, message=f"An unexpected error occurred: {e!s}", data=None)
