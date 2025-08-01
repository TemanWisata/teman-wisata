"""The main entry point for the Teman Wisata application."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Never

import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.core import CONFIG
from app.infrastructure import SupabaseClient


@asynccontextmanager
async def lifecycle(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: ARG001
    """Application lifecycle events."""

    def raise_supabase_config_error() -> Never:
        exception_message = "Supabase URL and key must be provided in the configuration."
        raise ValueError(exception_message)

    try:
        logger.info("Starting application...")
        if not all([CONFIG.supabase.url, CONFIG.supabase.key]):
            raise_supabase_config_error()
        key = CONFIG.supabase.key.get_secret_value() if CONFIG.supabase.key is not None else None
        await SupabaseClient.setup(CONFIG.supabase.url, key)
        yield
        SupabaseClient.reset()
        logger.info("Application shutdown complete.")
    except Exception as e:
        logger.error(f"An error occurred during application startup: {e}")
        raise
    finally:
        SupabaseClient.reset()
        logger.info("Supabase client has been reset.")


app = FastAPI(
    title="Teman Wisata API",
    description="API for the Teman Wisata application.",
    version=CONFIG.version,
    lifespan=lifecycle,
)


@app.get("/")
async def read_root() -> dict:
    """Root endpoint."""
    return {
        "message": "Welcome to the Teman Wisata API!",
        "version": CONFIG.version,
        "environment": CONFIG.environment,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=CONFIG.is_dev)
