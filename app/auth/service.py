"""Auth Service Module."""

from app.model import User
from supabase import AsyncClient


class UserService:
    """Service for handling authentication-related operations."""

    @staticmethod
    async def sign_up(client: AsyncClient, user_data: User) -> None:
        """Create a new user.

        :param client: Supabase client instance.
        :param user_data: User data to be inserted.

        """
        check_username = await client.table("users").select("username").eq("username", user_data.username).execute()
        if not check_username.data:
            exception_message = "Username already exists"
            raise ValueError(exception_message)

        await client.table("users").insert(user_data.model_dump()).execute()

    @staticmethod
    async def authenticate_user(client: AsyncClient, username: str, password: str) -> User | None:
        """Authenticate a user by username and password."""
        user = await client.table("users").select("*").eq("username", username).eq("password", password).execute()
        if not user.data:
            exception_message = "Invalid username or password"
            raise ValueError(exception_message)

        return User.model_validate(user.data[0])

    @staticmethod
    async def get_user_by_id(supabase: AsyncClient, user_id: str) -> None:
        """Get a user by user ID."""

    @staticmethod
    async def delete_user() -> None:
        """Delete a user by user ID."""
