#!/usr/bin/env python3
"""
Compliance Audit Script for AI Microservices
Verifies GDPR and 152-ФЗ compliance
"""

import re
from pathlib import Path
from typing import List, Dict, Any


class ComplianceAuditor:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.findings: List[Dict[str, Any]] = []
    
    def audit(self) -> List[Dict[str, Any]]:
        """Run all compliance checks"""
        self.check_gdpr_data_handling()
        self.check_152fz_data_localization()
        self.check_audit_logging()
        self.check_data_retention()
        self.check_privacy_controls()
        self.check_consent_mechanisms()
        self.check_incident_response()
        self.check_access_controls()
        return self.findings
    
    def check_gdpr_data_handling(self):
        """Check GDPR data handling compliance"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            # Pattern: PII data without encryption
            if "email" in content.lower() or "password" in content.lower():
                if "encrypt" not in content.lower() and "hash" not in content.lower():
                    self.add_finding(
                        "compliance",
                        "P1",
                        "PII data without encryption/hashing",
                        str(py_file),
                        0,
                        "Encrypt or hash PII data (GDPR Art. 32)",
                    )
    
    def check_152fz_data_localization(self):
        """Check 152-ФZ data localization compliance"""
        dockerfiles = list(self.project_root.rglob("Dockerfile"))
        for dockerfile in dockerfiles:
            content = dockerfile.read_text()
            # Pattern: non-Russian data centers
            if "aws" in content.lower() or "gcp" in content.lower():
                if "ru" not in content.lower():
                    self.add_finding(
                        "compliance",
                        "P1",
                        "Potential 152-ФZ violation - data not localized in Russia",
                        str(dockerfile),
                        0,
                        "Ensure data storage in Russian data centers (152-ФZ Art. 5)",
                    )
    
    def check_audit_logging(self):
        """Check for audit logging"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            if "delete" in content.lower() or "update" in content.lower():
                if "log" not in content.lower():
                    self.add_finding(
                        "compliance",
                        "P1",
                        "Data modification without audit logging",
                        str(py_file),
                        0,
                        "Add audit logging for data operations (GDPR Art. 30)",
                    )
    
    def check_data_retention(self):
        """Check data retention policies"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            if "database" in content.lower():
                if "retention" not in content.lower() and "delete" not in content.lower():
                    self.add_finding(
                        "compliance",
                        "P2",
                        "Missing data retention policy",
                        str(py_file),
                        0,
                        "Define data retention policy (GDPR Art. 5(1)(e))",
                    )
    
    def check_privacy_controls(self):
        """Check privacy controls"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            if "user" in content.lower():
                if "privacy" not in content.lower() and "consent" not in content.lower():
                    self.add_finding(
                        "compliance",
                        "P2",
                        "Missing privacy controls for user data",
                        str(py_file),
                        0,
                        "Implement privacy controls (GDPR Art. 25)",
                    )
    
    def check_consent_mechanisms(self):
        """Check consent mechanisms"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            if "personal" in content.lower() or "data" in content.lower():
                if "consent" not in content.lower():
                    self.add_finding(
                        "compliance",
                        "P1",
                        "Missing consent mechanism for data processing",
                        str(py_file),
                        0,
                        "Implement consent management (GDPR Art. 7)",
                    )
    
    def check_incident_response(self):
        """Check security incident response procedures"""
        # Check for incident response documentation
        md_files = list(self.project_root.rglob("*.md"))
        incident_doc = False
        for md_file in md_files:
            content = md_file.read_text().lower()
            if "incident" in content or "breach" in content:
                incident_doc = True
                break
        
        if not incident_doc:
            self.add_finding(
                "compliance",
                "P2",
                "Missing incident response documentation",
                "project",
                0,
                "Document incident response procedures (GDPR Art. 33)",
            )
    
    def check_access_controls(self):
        """Check access controls"""
        for py_file in self.project_root.rglob("*.py"):
            content = py_file.read_text()
            if "admin" in content.lower() or "delete" in content.lower():
                if "permission" not in content.lower() and "role" not in content.lower():
                    self.add_finding(
                        "compliance",
                        "P1",
                        "Sensitive operation without access control",
                        str(py_file),
                        0,
                        "Implement role-based access control (GDPR Art. 32)",
                    )
    
    def add_finding(self, finding_type: str, severity: str, title: str,
                    file: str, line: int, recommendation: str):
        self.findings.append({
            "id": f"COMP-{len(self.findings) + 1:03d}",
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
    auditor = ComplianceAuditor()
    findings = auditor.audit()
    print(f"Found {len(findings)} compliance issues")
    for finding in findings:
        print(f"[{finding['severity']}] {finding['title']} in {finding['file']}")
