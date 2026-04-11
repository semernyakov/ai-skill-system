"""AI Skill System - Main FastAPI Application"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from server.api.v1.audit import router as audit_router
from server.api.v1.logs import router as logs_router
from server.api.v1.mcp import router as mcp_router
from server.api.v1.rules import router as rules_router
from server.api.v1.skills import router as skills_router
from server.api.v1.sync import router as sync_router
from server.api.v1.auth import router as auth_router
from server.core.config import settings
from server.core.logging import setup_logging
from server.core.database import init_db
from server.core.rate_limit import get_health_rate_limiter, init_rate_limiter
from server.core.redis_client import init_redis
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database, Redis, and rate limiter on startup"""
    try:
        init_db()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    try:
        await init_redis()
        logger.info("Redis client initialized")
    except Exception as e:
        logger.warning(f"Failed to initialize Redis: {e}")
    try:
        await init_rate_limiter()
    except Exception as e:
        logger.warning(f"Failed to initialize rate limiter: {e}")


app.include_router(sync_router)
app.include_router(audit_router)
app.include_router(logs_router)
app.include_router(rules_router)
app.include_router(skills_router)
app.include_router(mcp_router)
app.include_router(auth_router)


@app.get("/", dependencies=[Depends(get_health_rate_limiter)])
async def root():
    return {"message": f"{settings.APP_NAME} v{settings.APP_VERSION}"}


@app.get("/health", dependencies=[Depends(get_health_rate_limiter)])
async def health():
    return {"status": "healthy"}
