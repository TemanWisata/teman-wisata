"""Dependency injection module for the Teman Wisata application."""

from typing import Annotated  # noqa: I001

from fastapi import Depends
from supabase import AsyncClient

from app.infrastructure.supabase_client import SupabaseClient

SupabaseClientDependency = Annotated[AsyncClient, Depends(SupabaseClient.get_client)]
