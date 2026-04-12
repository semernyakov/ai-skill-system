"""Database initialization script"""

import logging
import os
import sys

# Add server to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from server.core.database import init_db
from server.core.security import get_password_hash
from server.db.models import Rule, Skill, User, UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_admin_user():
    """Create default admin user"""
    from sqlmodel import Session

    from server.core.database import engine

    with Session(engine) as session:
        # Check if admin exists
        existing = session.get(User, "admin")
        if existing:
            logger.info("Admin user already exists")
            return

        # Create admin user (password: Admin123!)
        # Note: In production, change this immediately after first login
        admin = User(
            username="admin",
            hashed_password=get_password_hash("Admin123!"),
            role=UserRole.ADMIN
        )
        session.add(admin)
        session.commit()
        logger.info("Created admin user (username: admin)")


def create_default_rules():
    """Create default rules from .ai/rules/*.mdc files"""
    import json
    from pathlib import Path

    import yaml
    from sqlmodel import Session, select

    from server.core.database import engine

    with Session(engine) as session:
        # Check if rules already exist
        existing = session.exec(select(Rule)).all()
        if existing:
            logger.info(f"Rules already exist ({len(existing)} rules)")
            return

        rules_dir = Path(__file__).parent.parent.parent / ".ai" / "rules"
        if not rules_dir.exists():
            logger.warning(f"Rules directory not found: {rules_dir}")
            return

        default_rules = []
        for mdc_file in sorted(rules_dir.glob("*.mdc")):
            try:
                with open(mdc_file) as f:
                    content = f.read()
                    # Parse YAML frontmatter (between --- lines)
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 3:
                            frontmatter = yaml.safe_load(parts[1])
                            if isinstance(frontmatter, dict):
                                rule_name = mdc_file.stem  # Use filename as rule name
                                rule_data = {
                                    "name": rule_name,
                                    "description": frontmatter.get('description', ''),
                                    "globs": json.dumps(frontmatter.get('globs', [])),
                                    "always_apply": frontmatter.get('alwaysApply', False)
                                }
                                default_rules.append(rule_data)
            except Exception as e:
                logger.warning(f"Failed to parse {mdc_file}: {e}")
                continue

        for rule_data in default_rules:
            rule = Rule(**rule_data)
            session.add(rule)

        session.commit()
        logger.info(f"Created {len(default_rules)} default rules from .ai/rules/*.mdc")


def migrate_skill_model():
    """Migrate Skill model to add new fields"""
    from sqlmodel import Session, text

    from server.core.database import engine

    with Session(engine) as session:
        # Check if new columns exist
        result = session.exec(text("PRAGMA table_info(skill)")).all()
        columns = [row[1] for row in result]

        new_columns = {
            'config': "ALTER TABLE skill ADD COLUMN config TEXT DEFAULT '{}'",
            'source': "ALTER TABLE skill ADD COLUMN source VARCHAR(50) DEFAULT 'internal'",
            'version': "ALTER TABLE skill ADD COLUMN version VARCHAR(20)",
            'active': "ALTER TABLE skill ADD COLUMN active BOOLEAN DEFAULT 1"
        }

        for col_name, alter_sql in new_columns.items():
            if col_name not in columns:
                try:
                    session.exec(text(alter_sql))
                    session.commit()
                    logger.info(f"Added column '{col_name}' to skill table")
                except Exception as e:
                    logger.warning(f"Failed to add column '{col_name}': {e}")
                    session.rollback()


def create_default_skills():
    """Create default skills"""
    from sqlmodel import Session, select

    from server.core.database import engine

    with Session(engine) as session:
        # Check if skills already exist
        existing = session.exec(select(Skill)).all()
        if existing:
            logger.info(f"Skills already exist ({len(existing)} skills)")
            return

        default_skills = [
            {
                "name": "code-review",
                "description": "Review code for security vulnerabilities and best practices"
            },
            {
                "name": "performance-optimization",
                "description": "Analyze and optimize code performance"
            },
            {
                "name": "security-audit",
                "description": "Perform comprehensive security audit of the codebase"
            },
            {
                "name": "architecture-review",
                "description": "Review system architecture for scalability and maintainability"
            }
        ]

        for skill_data in default_skills:
            skill = Skill(**skill_data)
            session.add(skill)

        session.commit()
        logger.info(f"Created {len(default_skills)} default skills")


if __name__ == "__main__":
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized")
    create_admin_user()
    create_default_rules()
    migrate_skill_model()
    create_default_skills()
    logger.info("Done")
