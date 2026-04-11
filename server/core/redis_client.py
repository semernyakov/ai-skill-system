"""Redis client for shared state management"""

import json
import redis.asyncio as aioredis
from typing import Optional, Any
from server.core.config import settings

redis_client: Optional[aioredis.Redis] = None


async def init_redis():
    """Initialize Redis client"""
    global redis_client
    try:
        redis_client = await aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        await redis_client.ping()
        return True
    except Exception:
        return False


async def get_redis():
    """Get Redis client, initialize if needed"""
    global redis_client
    if redis_client is None:
        await init_redis()
    return redis_client


async def redis_get_json(key: str) -> Optional[Any]:
    """Get JSON data from Redis"""
    client = await get_redis()
    if client is None:
        return None
    try:
        data = await client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception:
        return None


async def redis_set_json(key: str, value: Any, expire: Optional[int] = None) -> bool:
    """Set JSON data in Redis"""
    client = await get_redis()
    if client is None:
        return False
    try:
        await client.set(key, json.dumps(value), ex=expire)
        return True
    except Exception:
        return False


async def redis_delete(key: str) -> bool:
    """Delete key from Redis"""
    client = await get_redis()
    if client is None:
        return False
    try:
        await client.delete(key)
        return True
    except Exception:
        return False


async def redis_list_append(key: str, value: Any) -> bool:
    """Append to a list in Redis"""
    client = await get_redis()
    if client is None:
        return False
    try:
        await client.lpush(key, json.dumps(value))
        return True
    except Exception:
        return False


async def redis_list_get_all(key: str) -> list:
    """Get all items from a Redis list"""
    client = await get_redis()
    if client is None:
        return []
    try:
        items = await client.lrange(key, 0, -1)
        return [json.loads(item) for item in items]
    except Exception:
        return []
