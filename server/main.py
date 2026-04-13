"""AI Skill System - Main FastAPI Application"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.api.v1.auth import router as auth_router
from server.api.v1.external_skills import router as external_skills_router
from server.api.v1.logs import router as logs_router
from server.api.v1.rules import router as rules_router
from server.api.v1.skills import router as skills_router
from server.core.config import settings
from server.core.database import init_db
from server.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler"""
    # Startup
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    yield
    # Shutdown
    logger.info("Shutting down")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(logs_router)
app.include_router(rules_router)
app.include_router(skills_router)
app.include_router(external_skills_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": f"{settings.APP_NAME} v{settings.APP_VERSION}"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
