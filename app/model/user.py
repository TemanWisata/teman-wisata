"""User model for the Teman Wisata application."""

from datetime import date

from pydantic import BaseModel, Field


class User(BaseModel):
    """User model for the application."""

    id: str = Field(description="Unique identifier for the user.")
    username: str = Field(description="Username of the user.")
    dob: date = Field(description="Date of birth of the user.")
    full_name: str | None = Field(default=None, description="Full name of the user.")
    province: str = Field(description="Province of the user.")
    created_at: str = Field(description="Timestamp when the user was created.")
    updated_at: str | None = Field(description="Timestamp when the user was last updated.")
    deleted_at: str | None = Field(default=None, description="Timestamp when the user was deleted, if applicable.")
