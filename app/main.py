"""The main entry point for the Teman Wisata application."""

import uvicorn
from fastapi import FastAPI

from app.core import CONFIG

app = FastAPI(
    title="Teman Wisata API",
    description="API for the Teman Wisata application.",
    version=CONFIG.version,
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
    uvicorn.run(app)
