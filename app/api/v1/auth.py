"""Router for authentication-related endpoints."""

from fastapi import APIRouter

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register() -> None:
    """Endpoint for user registration."""


@router.post("/login")
async def login() -> None:
    """Endpoint for user login."""


@router.post("/logout")
async def logout() -> None:
    """Endpoint for user logout."""


@router.get("/me")
async def get_me() -> None:
    """Endpoint for getting current user information."""
