"""Skill business logic service"""

import json
import logging
from datetime import datetime

from sqlmodel import Session, select

from server.db.models import Skill as SkillDB
from server.models.skill import Skill, SkillCreate, SkillUpdate

logger = logging.getLogger(__name__)


class SkillService:
    """Service for skill CRUD operations and execution"""

    def __init__(self, session: Session):
        self.session = session

    async def list_skills(self, active_only: bool = True) -> list[Skill]:
        """List all skills"""
        query = select(SkillDB)
        if active_only:
            query = query.where(SkillDB.active)
        skills = self.session.exec(query).all()
        return skills

    async def get_skill(self, skill_id: int) -> Skill | None:
        """Get skill by ID"""
        skill = self.session.get(SkillDB, skill_id)
        return skill

    async def create_skill(self, skill_data: SkillCreate) -> Skill:
        """Create new skill"""
        new_skill = SkillDB(
            name=skill_data.name,
            description=skill_data.description,
            config=json.dumps(skill_data.config),
            source=skill_data.source,
            version=skill_data.version,
            active=skill_data.active,
            created_at=datetime.now(),
        )
        self.session.add(new_skill)
        try:
            self.session.commit()
            self.session.refresh(new_skill)
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to create skill: {e}")
            raise
        return new_skill

    async def update_skill(self, skill_id: int, skill_data: SkillUpdate) -> Skill | None:
        """Update skill"""
        skill = self.session.get(SkillDB, skill_id)
        if not skill:
            return None

        update_data = skill_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "config" and value is not None:
                setattr(skill, key, json.dumps(value))
            else:
                setattr(skill, key, value)

        if update_data:
            skill.updated_at = datetime.now()

        self.session.add(skill)
        try:
            self.session.commit()
            self.session.refresh(skill)
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to update skill: {e}")
            raise
        return skill

    async def delete_skill(self, skill_id: int) -> bool:
        """Delete skill"""
        skill = self.session.get(SkillDB, skill_id)
        if not skill:
            return False

        self.session.delete(skill)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to delete skill: {e}")
            raise
        return True

    async def get_skill_config(self, skill_id: int) -> dict:
        """Get skill config as dict"""
        skill = await self.get_skill(skill_id)
        if not skill:
            return {}
        try:
            return json.loads(skill.config)
        except json.JSONDecodeError:
            return {}
