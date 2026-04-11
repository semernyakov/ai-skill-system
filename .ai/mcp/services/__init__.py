"""
MCP Service Adapters

This package contains adapters for various MCP services.
Each adapter implements the MCPServiceAdapter interface.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict


class MCPServiceAdapter(ABC):
    """Base interface for MCP service adapters."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize adapter with configuration."""
        self.config = config

    @abstractmethod
    async def invoke(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke MCP service method.

        Args:
            method: Service method name
            params: Method parameters

        Returns:
            Method result
        """
        pass

    @abstractmethod
    async def health(self) -> bool:
        """Check service health.

        Returns:
            True if service is healthy
        """
        pass

    @abstractmethod
    async def capabilities(self) -> Dict[str, Any]:
        """Return service capabilities.

        Returns:
            Dictionary of available methods and their schemas
        """
        pass
