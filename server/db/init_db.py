"""Database initialization script"""

import sys
import os

# Add server to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from server.core.database import init_db
from server.db.models import User, UserRole
from server.core.security import get_password_hash


def create_admin_user():
    """Create default admin user"""
    from sqlmodel import Session, select
    from server.core.database import engine
    
    with Session(engine) as session:
        # Check if admin exists
        existing = session.get(User, "admin")
        if existing:
            print("Admin user already exists")
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
        print("Created admin user (username: admin, password: admin123)")


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized")
    create_admin_user()
    print("Done")
