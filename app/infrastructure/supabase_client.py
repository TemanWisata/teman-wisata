"""Supabase client for the Teman Wisata application."""

from loguru import logger

from supabase import AsyncClient, acreate_client


class SupabaseClient:
    """Supabase client for the Teman Wisata application."""

    client: AsyncClient | None = None

    @classmethod
    async def test_connection(cls) -> bool:
        """Test the Supabase connection."""
        try:
            if cls.client is None:
                return False

            response = await cls.client.table("place").select("*").limit(1).execute()
        except Exception as e:  # noqa: BLE001
            logger.error(f"Supabase connection test failed: {e}")
            return False
        return response.data is not None

    @classmethod
    async def setup(cls, url: str | None, key: str | None) -> None:
        """Set up the Supabase client with the provided URL and key."""
        if url is None or key is None:
            exception_message = "Both URL and key must be provided to set up the Supabase client."
            raise ValueError(exception_message)

        if cls.client is None:
            cls.client = await acreate_client(url, key)

        else:
            exception_message = "Supabase client is already set up. If you need to reconfigure, please reset the client first."
            raise RuntimeError(exception_message)
        connection = await cls.test_connection()
        if connection:
            logger.success("Supabase client has been set up successfully.")
        else:
            exception_message = f"Failed to connect to Supabase. Please check your URL and key. Supabase Connection: {connection}"
            logger.error(exception_message)
            raise ConnectionError(exception_message)

    @classmethod
    def reset(cls) -> None:
        """Reset the Supabase client."""
        cls.client = None
        logger.info("Supabase client has been reset.")

    @classmethod
    def get_client(cls) -> AsyncClient:
        """Get the Supabase client."""
        exception_message = "Supabase client is not set up. Please call setup() first."
        if cls.client is None:
            raise RuntimeError(exception_message)
        return cls.client


def get_supabase_client() -> AsyncClient:
    """Get the Supabase client."""
    return SupabaseClient.get_client()
