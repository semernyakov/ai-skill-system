#!/usr/bin/env python3
"""
Performance Audit Script for AI Microservices
Analyzes performance bottlenecks
"""

import re
from pathlib import Path
from typing import List, Dict, Any


class PerformanceAuditor:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.findings: List[Dict[str, Any]] = []
    
    def audit(self) -> List[Dict[str, Any]]:
        """Run all performance checks"""
        self.check_n_plus_one_queries()
        self.check_missing_indexes()
        self.check_inefficient_loops()
        self.check_large_payloads()
        self.check_missing_caching()
        self.check_sync_operations()
        return self.findings
    
    def check_n_plus_one_queries(self):
        """Check for N+1 query patterns"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            # Pattern: loop inside loop with database calls
            if re.search(r'for\s+\w+\s+in.*:.*for\s+\w+\s+in.*:\s*\.query\(|\.execute\(', content, re.DOTALL):
                self.add_finding(
                    "performance",
                    "P1",
                    "Potential N+1 query pattern",
                    str(py_file),
                    0,
                    "Use eager loading or batch queries",
                )
    
    def check_missing_indexes(self):
        """Check for missing database indexes (basic heuristic)"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            if ".filter_by(" in content and "index" not in content.lower():
                self.add_finding(
                    "performance",
                    "P2",
                    "Query without index hint",
                    str(py_file),
                    0,
                    "Add database index for filtered fields",
                )
    
    def check_inefficient_loops(self):
        """Check for inefficient loop patterns"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            # Pattern: list.append in loop (should use list comprehension)
            if re.search(r'for\s+\w+\s+in.*:.*\.append\(', content, re.DOTALL):
                self.add_finding(
                    "performance",
                    "P2",
                    "Inefficient loop pattern",
                    str(py_file),
                    0,
                    "Use list comprehension or map",
                )
    
    def check_large_payloads(self):
        """Check for large payload transfers"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            if "response_model" in content and "List[" in content:
                self.add_finding(
                    "performance",
                    "P2",
                    "Potential large list response",
                    str(py_file),
                    0,
                    "Implement pagination",
                )
    
    def check_missing_caching(self):
        """Check for missing caching strategies"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            if "database" in content.lower() and "cache" not in content.lower():
                self.add_finding(
                    "performance",
                    "P2",
                    "Database query without caching",
                    str(py_file),
                    0,
                    "Add caching layer for frequent queries",
                )
    
    def check_sync_operations(self):
        """Check for synchronous I/O operations in async context"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            if "async def" in content and "requests.get" in content:
                self.add_finding(
                    "performance",
                    "P1",
                    "Synchronous HTTP in async function",
                    str(py_file),
                    0,
                    "Use async HTTP client (httpx/aiohttp)",
                )
    
    def add_finding(self, finding_type: str, severity: str, title: str,
                    file: str, line: int, recommendation: str):
        self.findings.append({
            "id": f"PERF-{len(self.findings) + 1:03d}",
            "type": finding_type,
            "severity": severity,
            "title": title,
            "file": file,
            "line": line,
            "description": title,
            "recommendation": recommendation,
            "references": []
        })


if __name__ == "__main__":
    auditor = PerformanceAuditor()
    findings = auditor.audit()
    print(f"Found {len(findings)} performance issues")
    for finding in findings:
        print(f"[{finding['severity']}] {finding['title']} in {finding['file']}")
