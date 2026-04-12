"""Centralized skill execution module"""

import logging
from typing import Any

from server.services.skill_service import SkillService

logger = logging.getLogger(__name__)


class SkillRunner:
    """Centralized skill execution runner"""

    def __init__(self, skill_service: SkillService):
        self.skill_service = skill_service

    async def execute(self, skill_id: int, input_data: dict[str, Any]) -> dict[str, Any]:
        """Execute skill with given input"""
        # Load skill from DB
        skill = await self.skill_service.get_skill(skill_id)
        if not skill:
            raise ValueError(f"Skill {skill_id} not found")

        if not skill.active:
            raise ValueError(f"Skill {skill_id} is not active")

        # Extract instructions from config
        config = await self.skill_service.get_skill_config(skill_id)
        instructions = config.get("instructions", "")

        # Inject user input
        # TODO: Integrate with LLM or MCP for actual execution
        # For now, return mock execution result
        result = {
            "skill_id": skill_id,
            "skill_name": skill.name,
            "input": input_data,
            "output": {
                "status": "executed",
                "message": f"Executed skill: {skill.name}",
                "instructions_used": bool(instructions)
            }
        }

        logger.info(f"Executed skill {skill_id} ({skill.name})")
        return result
