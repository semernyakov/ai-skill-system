"""AI Skill System - Main FastAPI Application"""

from fastapi import FastAPI

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

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# Initialize database
init_db()

app.include_router(sync_router)
app.include_router(audit_router)
app.include_router(logs_router)
app.include_router(rules_router)
app.include_router(skills_router)
app.include_router(mcp_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": f"{settings.APP_NAME} v{settings.APP_VERSION}"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
