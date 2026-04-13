"""FastAPI dependencies"""


from fastapi import Depends
from sqlmodel import Session

from server.core.config import settings
from server.core.database import get_session
from server.core.skill_runner import SkillRunner
from server.services.rule_service import RuleService
from server.services.skill_service import SkillService
from server.services.sync_service import SyncService


def get_settings():
    return settings


def get_skill_service(session: Session = Depends(get_session)):
    """Get skill service instance"""
    return SkillService(session)


def get_rule_service(session: Session = Depends(get_session)):
    """Get rule service instance"""
    return RuleService(session)


def get_skill_runner(skill_service: SkillService = Depends(get_skill_service)):
    """Get skill runner instance"""
    return SkillRunner(skill_service)


def get_sync_service(skill_service: SkillService = Depends(get_skill_service)):
    """Get sync service instance"""
    return SyncService(skill_service)
