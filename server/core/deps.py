"""FastAPI dependencies"""

from fastapi import Depends
from server.core.config import settings


def get_settings():
    return settings
