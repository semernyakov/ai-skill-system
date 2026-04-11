"""
Filesystem MCP Service Adapter

Provides file operations through MCP gateway.
"""
from pathlib import Path
from typing import Any, Dict
from . import MCPServiceAdapter


class FilesystemAdapter(MCPServiceAdapter):
    """Adapter for filesystem operations."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.allowed_paths = [Path(p).resolve() for p in config.get("allowed_paths", ["."])]
        self.read_only = config.get("read_only", False)

    def _is_path_allowed(self, path: Path) -> bool:
        """Check if path is within allowed directories."""
        try:
            resolved = path.resolve()
            for allowed in self.allowed_paths:
                if resolved == allowed or resolved.is_relative_to(allowed):
                    return True
            return False
        except Exception:
            return False

    async def invoke(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke filesystem method."""
        try:
            if method == "read_file":
                return await self._read_file(params)
            elif method == "write_file":
                return await self._write_file(params)
            elif method == "list_dir":
                return await self._list_dir(params)
            elif method == "delete_file":
                return await self._delete_file(params)
            else:
                return {"error": f"Unknown method: {method}"}
        except Exception as e:
            return {"error": str(e)}

    async def _read_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read file contents."""
        path = Path(params.get("path"))
        if not self._is_path_allowed(path):
            return {"error": "Path not allowed"}
        if not path.exists():
            return {"error": "File not found"}
        if not path.is_file():
            return {"error": "Not a file"}
        
        content = path.read_text()
        return {"content": content, "path": str(path)}

    async def _write_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Write file contents."""
        if self.read_only:
            return {"error": "Filesystem is read-only"}
        
        path = Path(params.get("path"))
        content = params.get("content", "")
        
        if not self._is_path_allowed(path):
            return {"error": "Path not allowed"}
        
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return {"success": True, "path": str(path)}

    async def _list_dir(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List directory contents."""
        path = Path(params.get("path", "."))
        if not self._is_path_allowed(path):
            return {"error": "Path not allowed"}
        if not path.exists():
            return {"error": "Path not found"}
        if not path.is_dir():
            return {"error": "Not a directory"}
        
        items = []
        for item in path.iterdir():
            items.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "path": str(item)
            })
        
        return {"items": items, "path": str(path)}

    async def _delete_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Delete file or directory."""
        if self.read_only:
            return {"error": "Filesystem is read-only"}
        
        path = Path(params.get("path"))
        if not self._is_path_allowed(path):
            return {"error": "Path not allowed"}
        if not path.exists():
            return {"error": "Path not found"}
        
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            import shutil
            shutil.rmtree(path)
        
        return {"success": True, "path": str(path)}

    async def health(self) -> bool:
        """Check filesystem health."""
        try:
            # Check if allowed paths exist
            for path in self.allowed_paths:
                if path.exists() or path.parent.exists():
                    return True
            return False
        except Exception:
            return False

    async def capabilities(self) -> Dict[str, Any]:
        """Return filesystem capabilities."""
        return {
            "methods": {
                "read_file": {
                    "description": "Read file contents",
                    "params": {"path": {"type": "string", "required": True}}
                },
                "write_file": {
                    "description": "Write file contents",
                    "params": {
                        "path": {"type": "string", "required": True},
                        "content": {"type": "string", "required": True}
                    }
                },
                "list_dir": {
                    "description": "List directory contents",
                    "params": {"path": {"type": "string", "required": False, "default": "."}}
                },
                "delete_file": {
                    "description": "Delete file or directory",
                    "params": {"path": {"type": "string", "required": True}}
                }
            },
            "read_only": self.read_only,
            "allowed_paths": [str(p) for p in self.allowed_paths]
        }
