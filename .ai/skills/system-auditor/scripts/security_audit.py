#!/usr/bin/env python3
"""
Security Audit Script for AI Microservices
Checks for common security vulnerabilities
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Any


class SecurityAuditor:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.findings: List[Dict[str, Any]] = []
    
    def audit(self) -> List[Dict[str, Any]]:
        """Run all security checks"""
        self.check_hardcoded_secrets()
        self.check_sql_injection()
        self.check_missing_auth()
        self.check_insecure_deps()
        self.check_exposed_debug()
        self.check_ssl_config()
        return self.findings
    
    def check_hardcoded_secrets(self):
        """Check for hardcoded API keys, passwords, tokens"""
        patterns = [
            (r'api[_-]?key\s*=\s*["\'][\w-]{20,}["\']', "Hardcoded API key"),
            (r'password\s*=\s*["\'][\w]+["\']', "Hardcoded password"),
            (r'secret[_-]?key\s*=\s*["\'][\w-]{20,}["\']', "Hardcoded secret key"),
            (r'token\s*=\s*["\'][\w-]{30,}["\']', "Hardcoded token"),
        ]
        
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            for pattern, desc in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    self.add_finding(
                        "security",
                        "P0",
                        desc,
                        str(py_file),
                        0,
                        "Move to environment variables",
                    )
    
    def check_sql_injection(self):
        """Check for SQL injection vulnerabilities"""
        patterns = [
            r'execute\(["\'].*\+.*["\']',
            r'execute\(f["\'].*\{.*\}.*["\']',
        ]
        
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    self.add_finding(
                        "security",
                        "P0",
                        "Potential SQL injection",
                        str(py_file),
                        0,
                        "Use parameterized queries",
                    )
    
    def check_missing_auth(self):
        """Check for missing authentication/authorization"""
        # Check FastAPI routes without auth decorators
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            if "@app.get" in content or "@app.post" in content:
                if "Depends" not in content and "auth" not in content.lower():
                    self.add_finding(
                        "security",
                        "P1",
                        "Route without authentication",
                        str(py_file),
                        0,
                        "Add authentication middleware",
                    )
    
    def check_insecure_deps(self):
        """Check for insecure dependencies (basic check)"""
        requirements_files = list(self.project_root.rglob("requirements*.txt"))
        for req_file in requirements_files:
            content = req_file.read_text()
            if "django<2" in content or "flask<1" in content:
                self.add_finding(
                    "security",
                    "P1",
                    "Outdated vulnerable dependency",
                    str(req_file),
                    0,
                    "Update to latest secure version",
                )
    
    def check_exposed_debug(self):
        """Check for exposed debug endpoints"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            if "debug=True" in content and "if __name__" not in content:
                self.add_finding(
                    "security",
                    "P1",
                    "Debug mode enabled in production",
                    str(py_file),
                    0,
                    "Disable debug in production",
                )
    
    def check_ssl_config(self):
        """Check SSL/TLS configuration"""
        dockerfiles = list(self.project_root.rglob("Dockerfile"))
        for dockerfile in dockerfiles:
            content = dockerfile.read_text()
            if "ssl" not in content.lower() and "tls" not in content.lower():
                self.add_finding(
                    "security",
                    "P2",
                    "No SSL/TLS configuration found",
                    str(dockerfile),
                    0,
                    "Configure SSL/TLS for production",
                )
    
    def add_finding(self, finding_type: str, severity: str, title: str, 
                    file: str, line: int, recommendation: str):
        self.findings.append({
            "id": f"SEC-{len(self.findings) + 1:03d}",
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
    auditor = SecurityAuditor()
    findings = auditor.audit()
    print(f"Found {len(findings)} security issues")
    for finding in findings:
        print(f"[{finding['severity']}] {finding['title']} in {finding['file']}")
