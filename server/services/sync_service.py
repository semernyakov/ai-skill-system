"""External skills sync service"""

import logging
from datetime import datetime
from pathlib import Path

import yaml

from server.services.skill_service import SkillService

logger = logging.getLogger(__name__)


class SyncService:
    """Service for syncing external skills from agentskills repository"""

    def __init__(self, skill_service: SkillService):
        self.skill_service = skill_service
        self.agentskills_path = Path(__file__).parent.parent.parent / "external" / "agentskills"

    async def run_sync(self) -> dict:
        """Run sync from external agentskills repository"""
        if not self.agentskills_path.exists():
            logger.warning(f"Agentskills path not found: {self.agentskills_path}")
            return {"status": "error", "message": "Agentskills repository not found"}

        skills_synced = 0
        skills_failed = 0

        # Scan for skill.yaml files
        for skill_dir in self.agentskills_path.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_yaml = skill_dir / "skill.yaml"
            if not skill_yaml.exists():
                continue

            try:
                skill_data = await self._parse_skill_yaml(skill_yaml, skill_dir)
                if skill_data:
                    await self._upsert_skill(skill_data)
                    skills_synced += 1
            except Exception as e:
                logger.error(f"Failed to sync skill from {skill_dir}: {e}")
                skills_failed += 1

        return {
            "status": "completed",
            "synced": skills_synced,
            "failed": skills_failed,
            "timestamp": datetime.now().isoformat()
        }

    async def _parse_skill_yaml(self, skill_yaml: Path, skill_dir: Path) -> dict | None:
        """Parse skill.yaml file"""
        with open(skill_yaml) as f:
            content = yaml.safe_load(f)

        if not isinstance(content, dict):
            return None

        # Extract instructions from prompt.md if exists
        prompt_md = skill_dir / "prompt.md"
        instructions = ""
        if prompt_md.exists():
            with open(prompt_md) as f:
                instructions = f.read()

        return {
            "name": content.get("name", skill_dir.name),
            "description": content.get("description", ""),
            "config": {
                "instructions": instructions,
                "input_schema": content.get("input_schema", {}),
                "output_schema": content.get("output_schema", {})
            },
            "source": "agentskills",
            "version": content.get("version"),
            "active": True
        }

    async def _upsert_skill(self, skill_data: dict):
        """Upsert skill to database"""
        from server.models.skill import SkillCreate

        # Check if skill exists by name and source
        existing_skills = await self.skill_service.list_skills(active_only=False)
        existing = next(
            (s for s in existing_skills if s.name == skill_data["name"] and s.source == skill_data["source"]),
            None
        )

        if existing:
            # Update existing skill
            from server.models.skill import SkillUpdate
            update_data = SkillUpdate(
                description=skill_data["description"],
                config=skill_data["config"],
                version=skill_data["version"],
                active=skill_data["active"]
            )
            await self.skill_service.update_skill(existing.id, update_data)
        else:
            # Create new skill
            create_data = SkillCreate(**skill_data)
            await self.skill_service.create_skill(create_data)
