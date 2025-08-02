"""User model for the Teman Wisata application."""

from datetime import date

from pydantic import UUID4, BaseModel, Field, SecretStr


class User(BaseModel):
    """User model for the application."""

    id: UUID4 = Field(description="Unique identifier for the user.")
    user_id: int = Field(description="Unique identifier for the user.")
    username: str = Field(description="Username of the user.")
    password: SecretStr = Field(description="Hashed password of the user.")
    dob: date = Field(description="Date of birth of the user.")
    full_name: str | None = Field(default=None, description="Full name of the user.")
    province: str = Field(description="Province of the user.")
    created_at: str | None = Field(description="Timestamp when the user was created.")
    updated_at: str | None = Field(description="Timestamp when the user was last updated.")
    deleted_at: str | None = Field(default=None, description="Timestamp when the user was deleted, if applicable.")


class SignUpRequest(BaseModel):
    """Request model for user sign-up."""

    username: str = Field(description="Username for the new user.")
    password: SecretStr = Field(description="Password for the new user.")
    dob: date = Field(description="Date of birth of the new user.")
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
