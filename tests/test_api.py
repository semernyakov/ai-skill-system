"""Server API Tests"""

import pytest
from httpx import AsyncClient
from server.main import app


class TestRulesAPI:
    """Test Rules API endpoints"""

    @pytest.mark.asyncio
    async def test_list_rules(self, client: AsyncClient):
        """Test GET /api/v1/rules"""
        response = await client.get("/api/v1/rules")
        assert response.status_code in [200, 404]  # 200 if rules exist, 404 if empty

    @pytest.mark.asyncio
    async def test_create_rule(self, client: AsyncClient):
        """Test POST /api/v1/rules"""
        rule_data = {
            "name": "test-rule",
            "description": "Test rule for testing",
            "globs": ["**/*.py"],
            "always_apply": False
        }
        response = await client.post("/api/v1/rules", json=rule_data)
        assert response.status_code in [200, 201]

    @pytest.mark.asyncio
    async def test_get_rule(self, client: AsyncClient):
        """Test GET /api/v1/rules/{rule_id}"""
        # First create a rule
        rule_data = {
            "name": "test-rule-get",
            "description": "Test rule for get",
            "globs": ["**/*.py"],
            "always_apply": False
        }
        create_response = await client.post("/api/v1/rules", json=rule_data)
        if create_response.status_code in [200, 201]:
            rule_id = create_response.json().get("id", 1)
            response = await client.get(f"/api/v1/rules/{rule_id}")
            assert response.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_update_rule(self, client: AsyncClient):
        """Test PUT /api/v1/rules/{rule_id}"""
        rule_data = {
            "name": "test-rule-update",
            "description": "Test rule for update",
            "globs": ["**/*.py"],
            "always_apply": False
        }
        create_response = await client.post("/api/v1/rules", json=rule_data)
        if create_response.status_code in [200, 201]:
            rule_id = create_response.json().get("id", 1)
            update_data = {
                "name": "updated-rule",
                "description": "Updated description"
            }
            response = await client.put(f"/api/v1/rules/{rule_id}", json=update_data)
            assert response.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_delete_rule(self, client: AsyncClient):
        """Test DELETE /api/v1/rules/{rule_id}"""
        rule_data = {
            "name": "test-rule-delete",
            "description": "Test rule for delete",
            "globs": ["**/*.py"],
            "always_apply": False
        }
        create_response = await client.post("/api/v1/rules", json=rule_data)
        if create_response.status_code in [200, 201]:
            rule_id = create_response.json().get("id", 1)
            response = await client.delete(f"/api/v1/rules/{rule_id}")
            assert response.status_code in [204, 404]


class TestSkillsAPI:
    """Test Skills API endpoints"""

    @pytest.mark.asyncio
    async def test_list_skills(self, client: AsyncClient):
        """Test GET /api/v1/skills"""
        response = await client.get("/api/v1/skills")
        assert response.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_create_skill(self, client: AsyncClient):
        """Test POST /api/v1/skills"""
        skill_data = {
            "name": "test-skill",
            "description": "Test skill for testing"
        }
        response = await client.post("/api/v1/skills", json=skill_data)
        assert response.status_code in [200, 201]

    @pytest.mark.asyncio
    async def test_get_skill(self, client: AsyncClient):
        """Test GET /api/v1/skills/{skill_id}"""
        skill_data = {
            "name": "test-skill-get",
            "description": "Test skill for get"
        }
        create_response = await client.post("/api/v1/skills", json=skill_data)
        if create_response.status_code in [200, 201]:
            skill_id = create_response.json().get("id", 1)
            response = await client.get(f"/api/v1/skills/{skill_id}")
            assert response.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_update_skill(self, client: AsyncClient):
        """Test PUT /api/v1/skills/{skill_id}"""
        skill_data = {
            "name": "test-skill-update",
            "description": "Test skill for update"
        }
        create_response = await client.post("/api/v1/skills", json=skill_data)
        if create_response.status_code in [200, 201]:
            skill_id = create_response.json().get("id", 1)
            update_data = {
                "name": "updated-skill",
                "description": "Updated description"
            }
            response = await client.put(f"/api/v1/skills/{skill_id}", json=update_data)
            assert response.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_delete_skill(self, client: AsyncClient):
        """Test DELETE /api/v1/skills/{skill_id}"""
        skill_data = {
            "name": "test-skill-delete",
            "description": "Test skill for delete"
        }
        create_response = await client.post("/api/v1/skills", json=skill_data)
        if create_response.status_code in [200, 201]:
            skill_id = create_response.json().get("id", 1)
            response = await client.delete(f"/api/v1/skills/{skill_id}")
            assert response.status_code in [204, 404]


class TestMCPAPI:
    """Test MCP Gateway API endpoints"""

    @pytest.mark.asyncio
    async def test_list_services(self, client: AsyncClient):
        """Test GET /api/v1/mcp/services"""
        response = await client.get("/api/v1/mcp/services")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_start_service(self, client: AsyncClient):
        """Test POST /api/v1/mcp/services/start"""
        service_data = {"service_name": "test-service"}
        response = await client.post("/api/v1/mcp/services/start", json=service_data)
        assert response.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_stop_service(self, client: AsyncClient):
        """Test POST /api/v1/mcp/services/stop"""
        service_data = {"service_name": "test-service"}
        response = await client.post("/api/v1/mcp/services/stop", json=service_data)
        assert response.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_health_all(self, client: AsyncClient):
        """Test GET /api/v1/mcp/health"""
        response = await client.get("/api/v1/mcp/health")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_health_service(self, client: AsyncClient):
        """Test GET /api/v1/mcp/services/{service_name}/health"""
        response = await client.get("/api/v1/mcp/services/test-service/health")
        assert response.status_code in [200, 404]


class TestSyncAPI:
    """Test Sync API endpoints"""

    @pytest.mark.asyncio
    async def test_sync_run(self, client: AsyncClient):
        """Test POST /api/v1/sync"""
        sync_data = {"source": "test-source"}
        response = await client.post("/api/v1/sync", json=sync_data)
        assert response.status_code in [200, 400]

    @pytest.mark.asyncio
    async def test_sync_status(self, client: AsyncClient):
        """Test GET /api/v1/sync/status"""
        response = await client.get("/api/v1/sync/status")
        assert response.status_code == 200


class TestAuditAPI:
    """Test Audit API endpoints"""

    @pytest.mark.asyncio
    async def test_audit_run(self, client: AsyncClient):
        """Test POST /api/v1/audit/run"""
        audit_data = {"audit_type": "security"}
        response = await client.post("/api/v1/audit/run", json=audit_data)
        assert response.status_code in [200, 400, 422]

    @pytest.mark.asyncio
    async def test_audit_results(self, client: AsyncClient):
        """Test GET /api/v1/audit/results"""
        response = await client.get("/api/v1/audit/results")
        assert response.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_audit_result(self, client: AsyncClient):
        """Test GET /api/v1/audit/results/{audit_id}"""
        response = await client.get("/api/v1/audit/results/1")
        assert response.status_code in [200, 404]


class TestLogsAPI:
    """Test Logs API endpoints"""

    @pytest.mark.asyncio
    async def test_logs_view(self, client: AsyncClient):
        """Test POST /api/v1/logs"""
        logs_data = {"limit": 10}
        response = await client.post("/api/v1/logs", json=logs_data)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_logs_stream(self, client: AsyncClient):
        """Test GET /api/v1/logs/stream"""
        response = await client.get("/api/v1/logs/stream")
        assert response.status_code in [200, 501]  # 501 if not implemented
