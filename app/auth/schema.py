"""Schema for Authentication-related operations."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, SecretStr


class SignUpRequest(BaseModel):
    """Request model for user sign-up."""

    username: str = Field(description="Username for the new user.")
    password: SecretStr = Field(description="Password for the new user.")
    dob: date = Field(description="Date of birth of the new user. Format: YYYY-MM-DD")
    full_name: str | None = Field(default=None, description="Full name of the new user.")
    province: str = Field(description="Province of the new user.")

    def set_hashed_password(self, hashed_password: str) -> None:
        """Set the hashed password for the user."""
        self.password = SecretStr(hashed_password)

    def model_dump(self, *args, **kwargs):  # noqa: ANN002, ANN003, ANN201
        """Override model_dump to handle SecretStr fields."""
        user_dict = super().model_dump(*args, **kwargs)
        # Convert SecretStr fields to their secret values
        if "password" in user_dict and isinstance(user_dict["password"], SecretStr):
            user_dict["password"] = user_dict["password"].get_secret_value()
        if "dob" in user_dict and isinstance(user_dict["dob"], date):
            user_dict["dob"] = user_dict["dob"].isoformat()
        return user_dict


class LoginRequest(BaseModel):
    """Request model for user login."""

    username: str = Field(description="Username for the user.")
    password: SecretStr = Field(description="Password for the user.")


class Token(BaseModel):
    """Model for authentication token."""

    access_token: SecretStr = Field(description="Access token for the user.")
    token_type: Literal["bearer"] | None = Field(default="bearer", description="Type of the token, usually 'bearer'.")

    def model_dump(self, *args, **kwargs) -> dict:  # noqa: ANN002, ANN003
        """Override model_dump to handle SecretStr fields."""
        token_dict = super().model_dump(*args, **kwargs)
        # Convert SecretStr fields to their secret values
        if "access_token" in token_dict and isinstance(token_dict["access_token"], SecretStr):
            token_dict["access_token"] = token_dict["access_token"].get_secret_value()
        return token_dict
