import json
from redis import asyncio

redis = asyncio.Redis.from_url(
    "redis://localhost:6379",
    decode_responses=True
)


async def cache_get(key: str):
    """Get cached value by key"""
    cached = await redis.get(key)
    if cached:
        return json.loads(cached)
    return None


async def cache_set(key: str, value, ttl: int = 300):
    """Set cached value by key with optional TTL (default 5 minutes)"""
    await redis.set(key, json.dumps(value), ex=ttl)


async def cache_delete(key: str):
    """Delete cached value by key"""
    await redis.delete(key)
