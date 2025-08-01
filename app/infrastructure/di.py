"""Dependency injection module for the Teman Wisata application."""

from typing import Annotated

from fastapi import Depends

from app.infrastructure.supabase_client import SupabaseClient

SupabaseClientDependency = Annotated[SupabaseClient, Depends(SupabaseClient.get_client)]
