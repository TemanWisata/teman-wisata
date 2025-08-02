"""User schema for the API."""

from datetime import date

from pydantic import BaseModel, Field, SecretStr


class AuthRequest(BaseModel):
    """Schema for Auth Request."""

    username: str = Field(
        description="User username",
    )
    password: SecretStr = Field(
        description="User password",
    )


class UserRegistration(BaseModel):
    """Schema for User Registration."""

    username: str = Field(
        description="Username for the new user",
    )
    password: SecretStr = Field(
        description="Password for the new user",
    )
    full_name: str = Field(
        description="Full name of the user",
    )
    dob: date = Field(
        description="Date of birth of the user",
    )
    province: str = Field(
        description="Province of the user",
    )
