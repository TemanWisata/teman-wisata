"""The main entry point for the Teman Wisata application."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Never

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from humanize import naturalsize
from loguru import logger
from psutil import cpu_count, cpu_percent, virtual_memory  # type: ignore  # noqa: PGH003
from scalar_fastapi import get_scalar_api_reference  # type: ignore  # noqa: PGH003

from app.api.v1 import auth_router
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
    docs_url=None,  # Disable Swagger UI
    redoc_url=None,  # Disable ReDoc
)


app.include_router(auth_router, prefix="/api/v1", tags=["auth"])


@app.get("/", include_in_schema=False)
async def read_root() -> JSONResponse:
    """Root endpoint."""
    return JSONResponse(
        content={
            "message": "Welcome to the Teman Wisata API!",
            "version": CONFIG.version,
            "environment": CONFIG.environment.name,
        },
    )


@app.get("/health", tags=["health"])
async def check_health() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse(
        content={
            "status": "healthy",
            "version": CONFIG.version,
            "environment": CONFIG.environment.name,
            "cpu_count": cpu_count(logical=True),
            "cpu_usage": cpu_percent(interval=1),
            "memory": {
                "total": naturalsize(virtual_memory().total),
                "available": naturalsize(virtual_memory().available),
                "used": naturalsize(virtual_memory().used),
                "percent": virtual_memory().percent,
            },
        },
    )


@app.get("/docs", include_in_schema=False)
async def scalar_docs() -> HTMLResponse:
    """Scalar documentation endpoint."""
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,  # type: ignore  # noqa: PGH003
        title=app.title,
    )
