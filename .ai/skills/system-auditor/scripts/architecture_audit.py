#!/usr/bin/env python3
"""
Architecture Audit Script for AI Microservices
Reviews architectural issues and design patterns
"""

import re
from pathlib import Path
from typing import List, Dict, Any


class ArchitectureAuditor:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.findings: List[Dict[str, Any]] = []
    
    def audit(self) -> List[Dict[str, Any]]:
        """Run all architecture checks"""
        self.check_circular_deps()
        self.check_tight_coupling()
        self.check_single_points_failure()
        self.check_over_engineering()
        self.check_separation_concerns()
        self.check_scalability()
        self.check_error_handling()
        return self.findings
    
    def check_circular_deps(self):
        """Check for circular dependencies (basic heuristic)"""
        imports = {}
        for py_file in self.project_root.rglob("*.py"):
            if "src" in str(py_file):
                content = py_file.read_text()
                module_imports = re.findall(r'from\s+(\S+)\s+import', content)
                imports[str(py_file)] = module_imports
        
        # Simple check: if A imports B and B imports A
        for file_a, modules_a in imports.items():
            for module in modules_a:
                file_b = self.project_root / f"{module.replace('.', '/')}.py"
                if file_b.exists() and file_b in imports:
                    if any(file_a in imp.replace('.', '/') for imp in imports[file_b]):
                        self.add_finding(
                            "architecture",
                            "P1",
                            "Circular dependency detected",
                            file_a,
                            0,
                            "Refactor to remove circular dependency",
                        )
    
    def check_tight_coupling(self):
        """Check for tight coupling between modules"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            # Pattern: many imports from same module
            if content.count("from app.") > 5:
                self.add_finding(
                    "architecture",
                    "P2",
                    "Tight coupling detected",
                    str(py_file),
                    0,
                    "Reduce coupling via interfaces/dependency injection",
                )
    
    def check_single_points_failure(self):
        """Check for single points of failure"""
        k8s_files = list(self.project_root.rglob("*.yaml"))
        for k8s_file in k8s_files:
            content = k8s_file.read_text()
            if "replicas: 1" in content:
                self.add_finding(
                    "architecture",
                    "P1",
                    "Single replica - potential SPOF",
                    str(k8s_file),
                    0,
                    "Set replicas >= 2 for high availability",
                )
    
    def check_over_engineering(self):
        """Check for over-engineering"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            # Pattern: excessive abstraction layers
            if content.count("class ") > 10 and len(content) < 500:
                self.add_finding(
                    "architecture",
                    "P3",
                    "Potential over-engineering",
                    str(py_file),
                    0,
                    "Simplify if abstraction not needed",
                )
    
    def check_separation_concerns(self):
        """Check for separation of concerns"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            # Pattern: business logic in routes
            if "@app." in content and content.count("def ") > 10:
                self.add_finding(
                    "architecture",
                    "P2",
                    "Business logic in route handler",
                    str(py_file),
                    0,
                    "Move business logic to service layer",
                )
    
    def check_scalability(self):
        """Check for scalability issues"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            # Pattern: in-memory state storage
            if "global " in content or "state = {}" in content:
                self.add_finding(
                    "architecture",
                    "P1",
                    "In-memory state - not scalable",
                    str(py_file),
                    0,
                    "Use external storage (Redis, database)",
                )
    
    def check_error_handling(self):
        """Check for error handling"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            # Pattern: functions without try/except
            func_defs = re.findall(r'def\s+\w+\([^)]*\):', content)
            if len(func_defs) > 3 and "try:" not in content:
                self.add_finding(
                    "architecture",
                    "P2",
                    "Missing error handling",
                    str(py_file),
                    0,
                    "Add try/except blocks for error handling",
                )
    
    def add_finding(self, finding_type: str, severity: str, title: str,
                    file: str, line: int, recommendation: str):
        self.findings.append({
            "id": f"ARCH-{len(self.findings) + 1:03d}",
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
    auditor = ArchitectureAuditor()
    findings = auditor.audit()
    print(f"Found {len(findings)} architecture issues")
    for finding in findings:
        print(f"[{finding['severity']}] {finding['title']} in {finding['file']}")
