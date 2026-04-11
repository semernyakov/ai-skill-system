#!/usr/bin/env python3
"""
Git Service Adapter for MCP Gateway

Provides git operations through MCP Gateway.
"""
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any


class GitAdapter:
    """Git service adapter for MCP Gateway"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.repo_path = Path(config.get("repo_path", ".")).resolve()
        
    async def invoke(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke git operation"""
        try:
            if method == "status":
                return await self._status()
            elif method == "commit":
                return await self._commit(params.get("message", ""), params.get("files", []))
            elif method == "push":
                return await self._push(params.get("remote", "origin"), params.get("branch", "master"))
            elif method == "pull":
                return await self._pull(params.get("remote", "origin"), params.get("branch", "master"))
            elif method == "add":
                return await self._add(params.get("files", []))
            elif method == "log":
                return await self._log(params.get("limit", 10))
            else:
                return {"error": f"Unknown method: {method}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def health(self) -> bool:
        """Check git health"""
        try:
            result = await self._run_git(["--version"])
            return result["exit_code"] == 0
        except Exception:
            return False
    
    async def capabilities(self) -> Dict[str, Any]:
        """Return git service capabilities"""
        return {
            "methods": ["status", "commit", "push", "pull", "add", "log"],
            "version": "1.0.0"
        }
    
    async def _run_git(self, args: list, cwd: Path = None) -> Dict[str, Any]:
        """Run git command"""
        try:
            if cwd is None:
                cwd = self.repo_path
            
            process = await asyncio.create_subprocess_exec(
                "git",
                *args,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            return {
                "exit_code": process.returncode,
                "stdout": stdout.decode("utf-8").strip(),
                "stderr": stderr.decode("utf-8").strip()
            }
        except Exception as e:
            return {
                "exit_code": -1,
                "stdout": "",
                "stderr": str(e)
            }
    
    async def _status(self) -> Dict[str, Any]:
        """Get git status"""
        result = await self._run_git(["status", "--porcelain"])
        if result["exit_code"] != 0:
            return {"error": result["stderr"]}
        
        files = []
        for line in result["stdout"].split("\n"):
            if line:
                status, file = line[:2], line[3:]
                files.append({"status": status, "file": file})
        
        return {"files": files, "branch": await self._get_current_branch()}
    
    async def _get_current_branch(self) -> str:
        """Get current branch name"""
        result = await self._run_git(["branch", "--show-current"])
        if result["exit_code"] == 0:
            return result["stdout"]
        return "unknown"
    
    async def _add(self, files: list) -> Dict[str, Any]:
        """Add files to staging"""
        if not files:
            return {"error": "No files specified"}
        
        args = ["add"] + files
        result = await self._run_git(args)
        
        if result["exit_code"] != 0:
            return {"error": result["stderr"]}
        
        return {"success": True, "files": files}
    
    async def _commit(self, message: str, files: list = None) -> Dict[str, Any]:
        """Commit changes"""
        if files:
            add_result = await self._add(files)
            if "error" in add_result:
                return add_result
        
        result = await self._run_git(["commit", "-m", message])
        
        if result["exit_code"] != 0:
            return {"error": result["stderr"]}
        
        return {"success": True, "message": message}
    
    async def _push(self, remote: str = "origin", branch: str = "master") -> Dict[str, Any]:
        """Push changes to remote"""
        result = await self._run_git(["push", remote, branch])
        
        if result["exit_code"] != 0:
            return {"error": result["stderr"]}
        
        return {"success": True, "remote": remote, "branch": branch}
    
    async def _pull(self, remote: str = "origin", branch: str = "master") -> Dict[str, Any]:
        """Pull changes from remote"""
        result = await self._run_git(["pull", remote, branch])
        
        if result["exit_code"] != 0:
            return {"error": result["stderr"]}
        
        return {"success": True, "remote": remote, "branch": branch}
    
    async def _log(self, limit: int = 10) -> Dict[str, Any]:
        """Get commit log"""
        result = await self._run_git(["log", f"-{limit}", "--pretty=format:%H|%s|%an|%ad", "--date=iso"])
        
        if result["exit_code"] != 0:
            return {"error": result["stderr"]}
        
        commits = []
        for line in result["stdout"].split("\n"):
            if line:
                hash_val, subject, author, date = line.split("|", 3)
                commits.append({
                    "hash": hash_val,
                    "subject": subject,
                    "author": author,
                    "date": date
                })
        
        return {"commits": commits}
