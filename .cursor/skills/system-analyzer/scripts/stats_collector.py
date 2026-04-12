#!/usr/bin/env python3
"""Collect system statistics for analysis."""
import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def should_skip(path: Path) -> bool:
    skip_patterns = [
        "node_modules", ".venv", "__pycache__", ".git",
        "build", "dist", ".ruff_cache", ".mypy_cache",
        ".pytest_cache", "*.egg-info"
    ]
    return any(p in path.parts for p in skip_patterns)


def count_loc(filepath: Path) -> int:
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            # Skip blank lines and simple comments
            code_lines = [
                l for l in lines 
                if l.strip() and not l.strip().startswith(("#", "//"))
            ]
            return len(code_lines)
    except Exception:
        return 0


def analyze_project(root: Path) -> dict:
    stats = defaultdict(lambda: {"files": 0, "loc": 0})
    total_files = 0
    max_depth = 0
    package_managers = set()
    
    for path in root.rglob("*"):
        if should_skip(path):
            continue
            
        if path.is_file():
            total_files += 1
            depth = len(path.relative_to(root).parts) - 1
            max_depth = max(max_depth, depth)
            
            # Detect package managers
            if path.name == "package.json":
                package_managers.add("npm")
            elif path.name in ("requirements.txt", "pyproject.toml"):
                package_managers.add("pip")
            elif path.name == "Cargo.toml":
                package_managers.add("cargo")
            elif path.name == "go.mod":
                package_managers.add("go")
            
            # Count by extension
            ext = path.suffix or "no_ext"
            if ext in (".py", ".js", ".ts", ".tsx", ".rs", ".go", ".md"):
                stats[ext]["files"] += 1
                stats[ext]["loc"] += count_loc(path)
    
    total_loc = sum(s["loc"] for s in stats.values())
    
    languages = [
        {
            "name": ext.lstrip(".").upper() if ext != "no_ext" else "OTHER",
            "files": s["files"],
            "loc": s["loc"],
            "percentage": round(s["loc"] / total_loc * 100, 1) if total_loc else 0
        }
        for ext, s in sorted(stats.items(), key=lambda x: -x[1]["loc"])
    ]
    
    return {
        "total_files": total_files,
        "total_loc": total_loc,
        "languages": languages,
        "max_depth": max_depth,
        "package_managers": sorted(package_managers)
    }


if __name__ == "__main__":
    root = Path(".")
    result = analyze_project(root)
    print(json.dumps(result, indent=2))
