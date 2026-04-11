"""Database initialization script"""

import sys
import os
import logging

# Add server to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from server.core.database import init_db
from server.db.models import User, UserRole
from server.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_admin_user():
    """Create default admin user"""
    from sqlmodel import Session, select
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


if __name__ == "__main__":
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized")
    create_admin_user()
    logger.info("Done")
