"""The main entry point for the Teman Wisata application."""

import uvicorn

from app.core import CONFIG

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=CONFIG.is_dev)
