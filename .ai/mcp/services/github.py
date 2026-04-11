#!/usr/bin/env python3
"""
GitHub Service Adapter for MCP Gateway

Provides GitHub API operations through MCP Gateway.
"""
import asyncio
import os
from typing import Dict, Any
from pathlib import Path


class GitHubAdapter:
    """GitHub service adapter for MCP Gateway"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_token = os.getenv("GITHUB_TOKEN") or config.get("api_token")
        self.default_owner = config.get("default_owner", "")
        self.base_url = "https://api.github.com"
        
    async def invoke(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke GitHub API operation"""
        try:
            if method == "get_repo":
                return await self._get_repo(params.get("owner", self.default_owner), params.get("repo"))
            elif method == "list_repos":
                return await self._list_repos(params.get("owner", self.default_owner))
            elif method == "create_issue":
                return await self._create_issue(
                    params.get("owner", self.default_owner),
                    params.get("repo"),
                    params.get("title"),
                    params.get("body"),
                    params.get("labels", [])
                )
            elif method == "get_issues":
                return await self._get_issues(params.get("owner", self.default_owner), params.get("repo"))
            elif method == "create_pull_request":
                return await self._create_pull_request(
                    params.get("owner", self.default_owner),
                    params.get("repo"),
                    params.get("title"),
                    params.get("body"),
                    params.get("head"),
                    params.get("base", "master")
                )
            else:
                return {"error": f"Unknown method: {method}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def health(self) -> bool:
        """Check GitHub API health"""
        try:
            # Simple health check - try to get user info
            import httpx
            async with httpx.AsyncClient() as client:
                headers = {}
                if self.api_token:
                    headers["Authorization"] = f"token {self.api_token}"
                
                response = await client.get(
                    f"{self.base_url}/user",
                    headers=headers,
                    timeout=5.0
                )
                return response.status_code == 200
        except Exception:
            return False
    
    async def capabilities(self) -> Dict[str, Any]:
        """Return GitHub service capabilities"""
        return {
            "methods": ["get_repo", "list_repos", "create_issue", "get_issues", "create_pull_request"],
            "version": "1.0.0"
        }
    
    async def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Make HTTP request to GitHub API"""
        import httpx
        
        url = f"{self.base_url}{endpoint}"
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        if self.api_token:
            headers["Authorization"] = f"token {self.api_token}"
        
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, headers=headers, timeout=10.0)
            elif method == "POST":
                response = await client.post(url, headers=headers, json=data, timeout=10.0)
            else:
                return {"error": f"Unsupported HTTP method: {method}"}
            
            if response.status_code == 200:
                return {"data": response.json()}
            else:
                return {
                    "error": f"HTTP {response.status_code}",
                    "message": response.text
                }
    
    async def _get_repo(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository information"""
        if not owner or not repo:
            return {"error": "owner and repo are required"}
        
        result = await self._make_request("GET", f"/repos/{owner}/{repo}")
        return result
    
    async def _list_repos(self, owner: str) -> Dict[str, Any]:
        """List repositories for an owner"""
        if not owner:
            return {"error": "owner is required"}
        
        result = await self._make_request("GET", f"/users/{owner}/repos")
        return result
    
    async def _create_issue(self, owner: str, repo: str, title: str, body: str = None, labels: list = None) -> Dict[str, Any]:
        """Create an issue"""
        if not owner or not repo or not title:
            return {"error": "owner, repo, and title are required"}
        
        data = {"title": title}
        if body:
            data["body"] = body
        if labels:
            data["labels"] = labels
        
        result = await self._make_request("POST", f"/repos/{owner}/{repo}/issues", data)
        return result
    
    async def _get_issues(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get issues for a repository"""
        if not owner or not repo:
            return {"error": "owner and repo are required"}
        
        result = await self._make_request("GET", f"/repos/{owner}/{repo}/issues")
        return result
    
    async def _create_pull_request(self, owner: str, repo: str, title: str, body: str = None, head: str = None, base: str = "master") -> Dict[str, Any]:
        """Create a pull request"""
        if not owner or not repo or not title:
            return {"error": "owner, repo, and title are required"}
        
        data = {"title": title, "base": base}
        if body:
            data["body"] = body
        if head:
            data["head"] = head
        
        result = await self._make_request("POST", f"/repos/{owner}/{repo}/pulls", data)
        return result
