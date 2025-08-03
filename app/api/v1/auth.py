"""Router for authentication-related endpoints."""

from datetime import timedelta

from fastapi import APIRouter, HTTPException, Request

from app.api.v1.schema import APIResponse
from app.auth import LoginRequest, SignUpRequest, Token, verify_bearer_token
from app.auth.service import OauthService, UserService
from app.core import CONFIG
from app.infrastructure.di import SupabaseClientDependency
from app.model import User

router = APIRouter(prefix="/auth")


@router.post("/register", description="Register a new user")
async def register(request: Request, supabase: SupabaseClientDependency, user_data: SignUpRequest) -> APIResponse:  # noqa: ARG001
    """Endpoint for user registration."""
    await UserService.sign_up(supabase, user_data)
    return APIResponse(success=True, message="User registered successfully")


@router.post("/login")
async def login(request: Request, supabase: SupabaseClientDependency, auth: LoginRequest) -> APIResponse[Token]:  # noqa: ARG001
    """Endpoint for user login."""
    try:
        user_data = await UserService.authenticate_user(supabase, username=auth.username, password=auth.password.get_secret_value())

        if not user_data:
            return APIResponse(success=False, message="Invalid username or password")

        token = OauthService.create_bearer_token(auth, expires_in=timedelta(minutes=CONFIG.oauth.access_token_expire_minutes))
        return APIResponse(success=True, message="User logged in successfully", data=token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/logout")
async def logout() -> None:
    """Endpoint for user logout."""


@router.get("/me")
async def get_me(request: Request, verify_user: verify_bearer_token) -> APIResponse[User]:  # noqa: ARG001
    """Endpoint for getting current user information."""
    return APIResponse(success=True, message="User information retrieved successfully", data=verify_user)


@router.put("/delete", description="Soft delete the current user")
async def delete_user(request: Request, verify_user: verify_bearer_token, supabase: SupabaseClientDependency) -> APIResponse:  # noqa: ARG001
    """Endpoint for deleting the current user."""
    try:
        await UserService.delete_user(supabase, uuid=verify_user.id)
        return APIResponse(success=True, message="User deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
