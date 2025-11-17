import os

import redis  # type: ignore

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL)


def get_redis() -> redis.Redis:
    """Возвращает клиент Redis."""
    return redis_client
