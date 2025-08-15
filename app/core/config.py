"""Config file for the Teman Wisata application."""

from enum import Enum

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.utils import Utils

class MlflowSettings(BaseSettings):
    """MLflow configuration settings."""

    model_uri: str | None = Field(
        default=None,
        description="The URI of the MLflow model.",
    )

    tracking_uri: str | None = Field(
        default=None,
        description="The URI of the MLflow tracking server.",
    )

    model_config = SettingsConfigDict(
        env_file=Utils.get_root_path().joinpath(".env"),
        env_file_encoding="utf-8",
        env_prefix="MLFLOW_",
        extra="allow",
        case_sensitive=False,
    )

class AWSSettings(BaseSettings):
    """AWS configuration settings."""

    access_key_id: str | None = Field(
        default=None,
        description="The AWS access key ID.",
    )
    secret_access_key: str | None = Field(
        default=None,
        description="The AWS secret access key.",
    )

    model_config = SettingsConfigDict(
        env_file=Utils.get_root_path().joinpath(".env"),
        env_file_encoding="utf-8",
        env_prefix="AWS_",
        extra="allow",
        case_sensitive=False,
    )

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


class OauthSettings(BaseSettings):
    """OAuth configuration settings."""

    secret_key: SecretStr | None = Field(default=None, description="The secret key for OAuth. From openssl rand -hex 32")
    algorithm: str | None = Field(default=None, description="The algorithm used for OAuth.")
    access_token_expire_minutes: float = Field(default=30.0, description="The expiration time for access tokens.")
    model_config = SettingsConfigDict(
        env_file=Utils.get_root_path().joinpath(".env"),
        env_file_encoding="utf-8",
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
    oauth: OauthSettings = Field(default_factory=OauthSettings, description="OAuth configuration settings.")
    mlflow: MlflowSettings = Field(default_factory=MlflowSettings, description="MLflow configuration settings.")
    aws: AWSSettings = Field(default_factory=AWSSettings, description="AWS configuration settings.")

    @property
    def version(self) -> str:
        """Get the project version."""
        return Utils.get_version()

    @property
    def is_dev(self) -> bool:
        """Check if the application is running in development mode."""
        return self.environment == Environment.DEV

    @property
    def is_production(self) -> bool:
        """Check if the application is running in production mode."""
        return self.environment == Environment.PRODUCTION


CONFIG = Config()
