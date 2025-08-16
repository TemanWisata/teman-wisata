"""Dependency injection module for the Teman Wisata application."""

from typing import Annotated  # noqa: I001

from fastapi import Depends
from supabase import AsyncClient
from redis.asyncio import Redis

from app.infrastructure.supabase_client import SupabaseClient
from app.infrastructure.redis_client import RedisClient

SupabaseClientDependency = Annotated[AsyncClient, Depends(SupabaseClient.get_client)]
RedisClientDependency = Annotated[Redis, Depends(RedisClient.get_client)]
