"""API version 1 endpoints."""

from .auth import router as auth_router

__all__ = [
    "auth_router",
]
