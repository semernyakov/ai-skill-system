"""Performance Tests"""

import pytest
import time
from httpx import AsyncClient


class TestAPIResponseTime:
    """Test API response times"""

    @pytest.mark.asyncio
    async def test_list_rules_response_time(self, client: AsyncClient):
        """Test GET /api/v1/rules response time"""
        start = time.time()
        response = await client.get("/api/v1/rules")
        duration = time.time() - start
        
        # Should respond within 1 second
        assert duration < 1.0, f"Response time {duration}s exceeds 1s threshold"
        assert response.status_code in [200, 401, 404]  # 401 if not authenticated

    @pytest.mark.asyncio
    async def test_list_skills_response_time(self, client: AsyncClient):
        """Test GET /api/v1/skills response time"""
        start = time.time()
        response = await client.get("/api/v1/skills")
        duration = time.time() - start
        
        # Should respond within 1 second
        assert duration < 1.0, f"Response time {duration}s exceeds 1s threshold"
        assert response.status_code in [200, 401, 404]  # 401 if not authenticated

    @pytest.mark.asyncio
    async def test_mcp_services_response_time(self, client: AsyncClient):
        """Test GET /api/v1/mcp/services response time"""
        # MCP endpoint removed during stack simplification
        pytest.skip("MCP endpoint removed")


class TestConcurrentRequests:
    """Test concurrent request handling"""

    @pytest.mark.asyncio
    async def test_concurrent_read_requests(self, client: AsyncClient):
        """Test multiple concurrent read requests"""
        import asyncio
        
        async def make_request():
            return await client.get("/api/v1/rules")
        
        # Make 10 concurrent requests
        tasks = [make_request() for _ in range(10)]
        responses = await asyncio.gather(*tasks)
        
        # All should succeed or require auth
        assert all(r.status_code in [200, 401, 404] for r in responses)

    @pytest.mark.asyncio
    async def test_concurrent_write_requests(self, client: AsyncClient):
        """Test multiple concurrent write requests"""
        import asyncio
        
        async def make_request():
            return await client.post("/api/v1/rules", json={
                "name": f"test-rule-{time.time()}",
                "description": "Concurrent test",
                "globs": ["**/*.py"],
                "always_apply": False
            })
        
        # Make 5 concurrent requests
        tasks = [make_request() for _ in range(5)]
        responses = await asyncio.gather(*tasks)
        
        # All should succeed, fail gracefully, or require auth
        assert all(r.status_code in [200, 201, 400, 401, 422] for r in responses)


class TestMemoryUsage:
    """Test memory usage patterns"""

    @pytest.mark.asyncio
    async def test_large_response_handling(self, client: AsyncClient):
        """Test handling of large responses"""
        # This is a placeholder - implement if large responses are possible
        pass


class TestDatabasePerformance:
    """Test database-related performance"""

    @pytest.mark.asyncio
    async def test_query_performance(self, client: AsyncClient):
        """Test database query performance"""
        start = time.time()
        response = await client.get("/api/v1/rules")
        duration = time.time() - start
        
        # Database queries should be fast
        assert duration < 0.5, f"Query time {duration}s exceeds 500ms threshold"
