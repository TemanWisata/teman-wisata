"""Dependency injection module for authentication services."""

from typing import Annotated

from fastapi import Depends

from app.auth.service import OauthService
from app.infrastructure.di import SupabaseClientDependency
from app.model import User


async def verify_authentication(
    supabase: SupabaseClientDependency,
    token: OauthService.bearer_dependency,  # type: ignore  # noqa: PGH003
) -> User:
    """Dependency to verify authentication using OAuth2."""
    return await OauthService.verify_bearer_token(supabase, token)


verify_bearer_token = Annotated[User, Depends(verify_authentication)]
