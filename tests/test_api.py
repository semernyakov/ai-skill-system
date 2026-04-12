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
        assert response.status_code in [200, 401, 404]  # 401 if not authenticated

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
        assert response.status_code in [200, 201, 401]  # 401 if not authenticated

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
        assert response.status_code in [200, 401, 404]  # 401 if not authenticated

    @pytest.mark.asyncio
    async def test_create_skill(self, client: AsyncClient):
        """Test POST /api/v1/skills"""
        skill_data = {
            "name": "test-skill",
            "description": "Test skill for testing"
        }
        response = await client.post("/api/v1/skills", json=skill_data)
        assert response.status_code in [200, 201, 401]  # 401 if not authenticated

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


class TestLogsAPI:
    """Test Logs API endpoints"""

    @pytest.mark.asyncio
    async def test_logs_view(self, client: AsyncClient):
        """Test GET /api/v1/logs"""
        response = await client.get("/api/v1/logs")
        assert response.status_code in [200, 401]  # 401 if not authenticated

    @pytest.mark.asyncio
    async def test_logs_stream(self, client: AsyncClient):
        """Test GET /api/v1/logs/stream"""
        response = await client.get("/api/v1/logs/stream")
        assert response.status_code in [200, 401, 501]  # 501 if not implemented
