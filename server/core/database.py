"""Database session management using SQLModel"""

from sqlmodel import Session, SQLModel, create_engine

from server.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)


def init_db():
    """Initialize database tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session
