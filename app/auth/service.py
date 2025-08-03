"""Auth Service Module."""

from datetime import datetime, timedelta, UTC  # noqa: I001
from typing import Annotated

from argon2 import PasswordHasher
from argon2.exceptions import HashingError, InvalidHashError, VerificationError, VerifyMismatchError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import SecretStr, TypeAdapter, UUID4
from supabase import AsyncClient
from authlib.jose import jwt, JoseError  # type: ignore  # noqa: PGH003
from loguru import logger

from app.model import User
from app.auth.schema import SignUpRequest, LoginRequest, Token
from app.core import CONFIG


class OauthService:
    """Service for handling OAuth-related operations."""

    bearer_dependency = Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]

    @staticmethod
    def create_bearer_token(login_request: LoginRequest, expires_in: timedelta | None) -> Token:
        """Create a bearer token for the user."""
        try:
            to_encode = login_request.model_dump()
            to_encode.pop("password", None)  # Remove password from payload
            now = int(datetime.now(UTC).timestamp())
            expire = datetime.now(UTC) + (expires_in or timedelta(minutes=CONFIG.oauth.access_token_expire_minutes))  # type: ignore  # noqa: PGH003
            to_encode.update({"exp": int(expire.timestamp()), "iat": now, "nbf": now})

            header = {"alg": CONFIG.oauth.algorithm}
            encoded_jwt = jwt.encode(header, to_encode, CONFIG.oauth.secret_key.get_secret_value())  # type: ignore  # noqa: PGH003
            return Token(
                access_token=encoded_jwt.decode("utf-8") if isinstance(encoded_jwt, bytes) else encoded_jwt,
            )

        except JoseError as e:
            logger.error(f"Error creating token: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating token") from e
        except Exception as e:
            exception_message = f"An unexpected error occurred during token creation: {e}"
            logger.error(exception_message)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exception_message) from e

    @staticmethod
    async def verify_bearer_token(supabase: AsyncClient, credential: HTTPAuthorizationCredentials) -> User:
        """Verify the bearer token and return the user."""
        try:
            token = credential.credentials
            logger.debug(f"Token received for verification: {token}")
            claims = jwt.decode(token, CONFIG.oauth.secret_key.get_secret_value())  # type: ignore  # noqa: PGH003
            claims.validate()  # This checks exp, nbf, etc.
            username = claims.get("username")
            if not username:
                logger.error("Invalid token payload: 'username' not found")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")  # noqa: TRY301
            return await UserService.get_user_by_username(supabase=supabase, username=username)
        except JoseError as e:
            logger.error(f"Invalid or expired token: {e}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from e
        except Exception as e:
            exception_message = f"An unexpected error occurred during token verification: {e}"
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exception_message) from e


class AuthPasswordService:
    """Service for handling password-related operations."""

    ph = PasswordHasher()

    @classmethod
    def hash_password(cls, password: SecretStr) -> str:
        """Hash the password."""
        try:
            return cls.ph.hash(password.get_secret_value())
        except HashingError as e:
            raise HTTPException(status_code=500, detail="Internal server error") from e
        except Exception as e:
            exception_message = f"An unexpected error occurred during password hashing: {e}"
            raise HTTPException(status_code=500, detail=exception_message) from e

    @classmethod
    def verify_password(cls, plain_password: SecretStr, hashed_password: SecretStr) -> bool:
        """Verify the password against the hashed password."""
        try:
            return cls.ph.verify(hashed_password.get_secret_value(), plain_password.get_secret_value())
        except VerifyMismatchError as e:
            raise HTTPException(status_code=401, detail="Username or password is incorrect") from e
        except (InvalidHashError, VerificationError) as e:
            raise HTTPException(status_code=500, detail="Internal server error") from e
        except Exception as e:
            exception_message = f"An unexpected error occurred during password verification: {e}"
            raise HTTPException(status_code=500, detail=exception_message) from e


class UserService:
    """Service for handling authentication-related operations."""

    @staticmethod
    async def sign_up(client: AsyncClient, user_data: SignUpRequest) -> None:
        """Create a new user.

        :param client: Supabase client instance.
        :param user_data: User data to be inserted.

        """
        try:
            check_username = await client.table("users").select("username").eq("username", user_data.username).execute()
            if check_username.data:
                exception_message = "Username already exists"
                raise ValueError(exception_message)  # noqa: TRY301
            hashed_password = AuthPasswordService.hash_password(user_data.password)
            user_data.set_hashed_password(hashed_password)
            user_dict = user_data.model_dump()

            await client.table("users").insert(user_dict).execute()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            exception_message = f"An unexpected error occurred during user sign-up: {e}"
            raise HTTPException(status_code=500, detail=exception_message) from e

    @staticmethod
    async def authenticate_user(client: AsyncClient, username: str, password: str) -> User | None:
        """Authenticate a user by username and password."""
        try:
            user = await client.table("users").select("*").eq("username", username).execute()
            if not user.data:
                raise HTTPException(status_code=401, detail="Username or password is incorrect")  # noqa: TRY301
            user_data = TypeAdapter(User).validate_python(user.data[0]) if user.data else None

            if not user_data or not AuthPasswordService.verify_password(SecretStr(password), user_data.password):
                raise HTTPException(status_code=401, detail="Username or password is incorrect")  # noqa: TRY301

            return user_data  # noqa: TRY300
        except HTTPException:
            raise
        except Exception as e:
            exception_message = f"An unexpected error occurred during user authentication: {e}"
            raise HTTPException(status_code=500, detail=exception_message) from e

    @staticmethod
    async def get_user_by_username(supabase: AsyncClient, username: str) -> User:
        """Get a user by username."""
        try:
            user = await supabase.table("users").select("*").eq("username", username).execute()
            if not user.data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")  # noqa: TRY301
            return TypeAdapter(User).validate_python(user.data[0])
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail) from e
        except Exception as e:
            exception_message = f"An unexpected error occurred while fetching the user: {e}"
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exception_message) from e

    @staticmethod
    async def delete_user(supabase: AsyncClient, uuid: UUID4) -> None:
        """Delete a user by user ID."""
        try:
            deleted_at = datetime.now(UTC).isoformat()
            await supabase.table("users").update({"deleted_at": deleted_at}).eq("id", uuid).execute()
            logger.success(f"User with ID {uuid} soft deleted successfully")
        except Exception as e:
            exception_message = f"An unexpected error occurred while deleting the user: {e}"
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exception_message) from e
