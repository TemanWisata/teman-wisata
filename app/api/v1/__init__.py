"""API version 1 endpoints."""

from .auth import router as auth_router
from .place import router as place_router
from .recommender import router as recommender_router

__all__ = [
    "auth_router",
    "place_router",
    "recommender_router",
]
