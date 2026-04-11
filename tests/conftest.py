"""Pytest configuration and fixtures"""

import pytest
import sys
import os
from httpx import AsyncClient, ASGITransport
from server.main import app

# Add server to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
async def client():
    """Async HTTP client for testing"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
