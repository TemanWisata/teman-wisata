"""Module for Recommender API."""

import json

import pandas as pd  # noqa: TC002
from fastapi import APIRouter, Request
from loguru import logger
from pydantic import TypeAdapter

from app.api.v1.schema.api_response import APIResponse
from app.auth.di import verify_bearer_token
from app.infrastructure.di import RedisClientDependency, SupabaseClientDependency
from app.place.schema import RecommendedPlace
from app.place.service import PlaceService
from app.recommender.schema import RecommenderRequest
from app.recommender.service import RecommenderService

router = APIRouter(
    prefix="/recommender",
    responses={404: {"description": "Not found"}},
)


@router.post("/user/")
async def get_user_ratings(
    request: Request,  # noqa: ARG001
    recommender_request: RecommenderRequest,
    supabase_client: SupabaseClientDependency,
    redis_client: RedisClientDependency,
    user: verify_bearer_token,
) -> APIResponse[RecommendedPlace]:
    """Get user ratings DataFrame."""
    is_user_already_rate = await PlaceService.check_if_user_rate(supabase_client, user_id=user.user_id)
    if not is_user_already_rate:
        logger.warning(f"User {user.user_id} has not rated any places yet.")
        return APIResponse(
            success=False,
            http_status=400,
            message="User has not rated any places yet.",
            data=RecommendedPlace(data=[]),
        )
    cache_key = f"user:{user.user_id}:{user.id}:{recommender_request.k}:{int(recommender_request.filter_viewed)}:recommendations"
    cached_places = await redis_client.get(cache_key)
    if cached_places:
        logger.info(f"Cache hit for user {user.user_id} recommendations.")
        cached_places_data = json.loads(cached_places)
        model_data = TypeAdapter(RecommendedPlace).validate_python(cached_places_data)
        return APIResponse(success=True, http_status=200, message="Get recommendation from cache", data=model_data)
    df = await PlaceService.get_all_user_place_ratings_df(supabase_client)
    rectools_dataset = RecommenderService.get_df_user_ratings(dataframe=df)
    logger.info(f"User {user.user_id} ratings DataFrame retrieved successfully.")
    result: pd.DataFrame = RecommenderService.recommend(user_id=[user.user_id], dataset=rectools_dataset, k=recommender_request.k, filter_viewed=recommender_request.filter_viewed)  # type: ignore  # noqa: PGH003
    list_of_place_id = result["item_id"].astype(int).tolist()
    places: RecommendedPlace = await PlaceService.get_place_by_list_id(supabase_client, place_ids=list_of_place_id)
    places_dict = places.model_dump()
    logger.info(f"User {user.user_id} recommendations generated successfully.")
    await redis_client.set(cache_key, json.dumps(places_dict), ex=300)
    return APIResponse(success=True, http_status=200, message="Get recommendations success", data=places)
