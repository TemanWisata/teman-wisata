"""Auth Service Module."""

from argon2 import PasswordHasher  # noqa: I001
from argon2.exceptions import HashingError, InvalidHashError, VerificationError, VerifyMismatchError
from fastapi import HTTPException
from pydantic import SecretStr, TypeAdapter
from supabase import AsyncClient

from app.model import User, SignUpRequest


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
    async def get_user_by_id(supabase: AsyncClient, user_id: str) -> None:
        """Get a user by user ID."""

    @staticmethod
    async def delete_user() -> None:
        """Delete a user by user ID."""
