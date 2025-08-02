"""Router for authentication-related endpoints."""

from fastapi import APIRouter, Request

from app.api.v1.schema import APIResponse
from app.auth.service import UserService
from app.infrastructure.di import SupabaseClientDependency
from app.model import LoginRequest, SignUpRequest

router = APIRouter(prefix="/auth")


@router.post("/register", description="Register a new user")
async def register(request: Request, supabase: SupabaseClientDependency, user_data: SignUpRequest) -> APIResponse:  # noqa: ARG001
    """Endpoint for user registration."""
    await UserService.sign_up(supabase, user_data)
    return APIResponse(success=True, message="User registered successfully")


@router.post("/login")
async def login(request: Request, supabase: SupabaseClientDependency, auth: LoginRequest) -> APIResponse:  # noqa: ARG001
    """Endpoint for user login."""
    await UserService.authenticate_user(supabase, username=auth.username, password=auth.password.get_secret_value())
    return APIResponse(success=True, message="User logged in successfully")


@router.post("/logout")
async def logout() -> None:
    """Endpoint for user logout."""


@router.get("/me")
async def get_me() -> None:
    """Endpoint for getting current user information."""
