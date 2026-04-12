"""Rate limiting configuration using fastapi-limiter with Redis backend"""

from pyrate_limiter import Duration, Limiter, Rate
from fastapi import Request
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as aioredis
from server.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Define rate limits
auth_limiter = Limiter(Rate(20, Duration.MINUTE))  # 20 req/min for auth
read_limiter = Limiter(Rate(100, Duration.MINUTE))  # 100 req/min for reads
write_limiter = Limiter(Rate(20, Duration.MINUTE))  # 20 req/min for writes
health_limiter = Limiter(Rate(1000, Duration.MINUTE))  # 1000 req/min for health

# Custom rate limiter that skips OPTIONS requests
class CORSRateLimiter(RateLimiter):
    async def __call__(self, request: Request):
        # Skip rate limiting for OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            return
        await super().__call__(request)

# Rate limiter dependency factories
def get_auth_rate_limiter():
    return CORSRateLimiter(limiter=auth_limiter)

def get_read_rate_limiter():
    return CORSRateLimiter(limiter=read_limiter)

def get_write_rate_limiter():
    return CORSRateLimiter(limiter=write_limiter)

def get_health_rate_limiter():
    return CORSRateLimiter(limiter=health_limiter)

async def init_rate_limiter():
    """Initialize rate limiter with Redis backend"""
    try:
        redis = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
        # RateLimiter uses Redis automatically when configured
        logger.info(f"Rate limiter initialized with Redis at {settings.REDIS_URL}")
    except Exception as e:
        logger.warning(f"Failed to initialize Redis rate limiter: {e}. Using in-memory fallback.")
        logger.warning("Rate limiting will not work correctly with multiple workers.")
