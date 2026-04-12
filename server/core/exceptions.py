"""Custom exceptions for the application"""


class SkillNotFoundError(Exception):
    """Raised when a skill is not found"""
    pass


class SyncError(Exception):
    """Raised when skill sync fails"""
    pass


class ExecutionError(Exception):
    """Raised when skill execution fails"""
    pass


class ValidationError(Exception):
    """Raised when input validation fails"""
    pass
