"""Rule business logic service"""

import json
import logging
from datetime import datetime

from sqlmodel import Session, select

from server.db.models import Rule as RuleDB
from server.models.rule import Rule, RuleCreate, RuleUpdate

logger = logging.getLogger(__name__)


class RuleService:
    """Service for rule CRUD operations"""

    def __init__(self, session: Session):
        self.session = session

    async def list_rules(self) -> list[Rule]:
        """List all rules"""
        rules = self.session.exec(select(RuleDB)).all()
        result = []
        for r in rules:
            try:
                globs = json.loads(r.globs) if r.globs else []
            except json.JSONDecodeError:
                globs = []
            result.append(
                Rule(
                    id=r.id,
                    name=r.name,
                    description=r.description,
                    globs=globs,
                    always_apply=r.always_apply,
                    created_at=r.created_at,
                    updated_at=r.updated_at
                )
            )
        return result

    async def get_rule(self, rule_id: int) -> Rule | None:
        """Get rule by ID"""
        rule = self.session.get(RuleDB, rule_id)
        if not rule:
            return None
        try:
            globs = json.loads(rule.globs) if rule.globs else []
        except json.JSONDecodeError:
            globs = []
        return Rule(
            id=rule.id,
            name=rule.name,
            description=rule.description,
            globs=globs,
            always_apply=rule.always_apply,
            created_at=rule.created_at,
            updated_at=rule.updated_at
        )

    async def create_rule(self, rule_data: RuleCreate) -> Rule:
        """Create new rule"""
        new_rule = RuleDB(
            name=rule_data.name,
            description=rule_data.description,
            globs=json.dumps(rule_data.globs),
            always_apply=rule_data.always_apply,
            created_at=datetime.now(),
        )
        self.session.add(new_rule)
        try:
            self.session.commit()
            self.session.refresh(new_rule)
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to create rule: {e}")
            raise
        return Rule(
            id=new_rule.id,
            name=new_rule.name,
            description=new_rule.description,
            globs=rule_data.globs,
            always_apply=new_rule.always_apply,
            created_at=new_rule.created_at,
            updated_at=new_rule.updated_at
        )

    async def update_rule(self, rule_id: int, rule_data: RuleUpdate) -> Rule | None:
        """Update rule"""
        rule = self.session.get(RuleDB, rule_id)
        if not rule:
            return None

        update_data = rule_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == 'globs' and value is not None:
                setattr(rule, key, json.dumps(value))
            else:
                setattr(rule, key, value)

        if update_data:
            rule.updated_at = datetime.now()

        self.session.add(rule)
        try:
            self.session.commit()
            self.session.refresh(rule)
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to update rule: {e}")
            raise

        try:
            globs = json.loads(rule.globs) if rule.globs else []
        except json.JSONDecodeError:
            globs = []
        return Rule(
            id=rule.id,
            name=rule.name,
            description=rule.description,
            globs=globs,
            always_apply=rule.always_apply,
            created_at=rule.created_at,
            updated_at=rule.updated_at
        )

    async def delete_rule(self, rule_id: int) -> bool:
        """Delete rule"""
        rule = self.session.get(RuleDB, rule_id)
        if not rule:
            return False

        self.session.delete(rule)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to delete rule: {e}")
            raise
        return True
