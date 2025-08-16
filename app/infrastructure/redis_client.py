"""Redis Client."""

from loguru import logger
from redis.asyncio import Redis


class RedisClient:
    """Redis Client."""

    client: Redis | None = None

    @classmethod
    def initialize(cls, redis_url: str) -> None:
        """Initialize the Redis client."""
        try:
            if not cls.client:
                logger.info("Initializing Redis client")
                cls.client = Redis.from_url(url=redis_url)
                logger.success("Redis client initialized successfully")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Failed to initialize Redis client: {e}")
            cls.client = None

    @classmethod
    async def close(cls) -> None:
        """Close the Redis client."""
        if cls.client:
            try:
                logger.info("Closing Redis client")
                await cls.client.close()
                logger.info("Redis client closed successfully")
            except Exception as e:  # noqa: BLE001
                logger.error(f"Failed to close Redis client: {e}")
            finally:
                cls.client = None

    @classmethod
    def get_client(cls) -> Redis | None:
        """Get the Redis client."""
        if cls.client is None:
            logger.warning("Redis client is not initialized")
            return None
        return cls.client

    @classmethod
    async def check_connection(cls) -> bool:
        """Check if the Redis client is connected."""
        if cls.client:
            try:
                return await cls.client.ping()
            except Exception as e:  # noqa: BLE001
                logger.error(f"Redis connection check failed: {e}")
                return False
        logger.warning("Redis client is not initialized")
        return False
