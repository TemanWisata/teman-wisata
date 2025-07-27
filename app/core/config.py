"""Config file for the Teman Wisata application."""

from enum import Enum

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.utils import Utils


class SupabaseSettings(BaseSettings):
    """Supabase configuration settings."""

    url: str | None = Field(default=None, description="The URL of the Supabase instance.")
    key: SecretStr | None = Field(
        default=None,
        description="The secret key for accessing the Supabase instance.",
    )
    model_config = SettingsConfigDict(
        env_file=Utils.get_root_path().joinpath(".env"),
        env_file_encoding="utf-8",
        env_prefix="SUPABASE_",
        extra="allow",
        case_sensitive=False,
    )


class Environment(Enum):
    """Enumeration for different environments."""

    DEV = "dev"
    PRODUCTION = "prod"


class Config(BaseSettings):
    """Main configuration class for the application."""

    environment: Environment = Field(default=Environment.DEV, description="The environment in which the application is running.")
    supabase: SupabaseSettings = Field(default_factory=SupabaseSettings, description="Supabase configuration settings.")
    model_config = SettingsConfigDict(
        env_file=Utils.get_root_path().joinpath(".env"),
        env_file_encoding="utf-8",
        extra="allow",
        case_sensitive=False,
    )

    @property
    def version(self) -> str:
        """Get the project version."""
        return Utils.get_version()


CONFIG = Config()
