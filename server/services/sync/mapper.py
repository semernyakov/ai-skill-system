"""Map external skill data to internal Skill model"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class SkillMapper:
    """Map external skill data to internal Skill model"""

    def map_to_skill_create(self, skill_data: dict[str, Any], instructions: str) -> dict[str, Any]:
        """Map parsed skill data to SkillCreate format"""
        return {
            "name": skill_data.get("name", ""),
            "description": skill_data.get("description", ""),
            "config": {
                "instructions": instructions,
                "input_schema": skill_data.get("input_schema", {}),
                "output_schema": skill_data.get("output_schema", {})
            },
            "source": "agentskills",
            "version": skill_data.get("version"),
            "active": True
        }
