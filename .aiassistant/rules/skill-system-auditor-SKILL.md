<!-- PyCharm AI Skill Reference -->
<!-- Source: .ai/skills/system-auditor/SKILL.md -->
<!-- Synced: Sun Apr 12 20:37:06 MSK 2026 -->
<!-- Rule type: Manually (trigger by name) -->

---
name: system-auditor
description: >
  Comprehensive system audit for AI microservices covering security, performance, architecture, and compliance.
  Use when user requests "audit system", "security check", "performance review", "architecture review", "compliance audit",
  or mentions keywords like "audit", "check security", "test performance", "review architecture", "verify compliance".
  Trigger on phrases like "audit my system", "check for vulnerabilities", "analyze performance", "review code architecture",
  "compliance check", "security audit", "performance bottleneck", "architectural issues", "GDPR compliance", "152-ФЗ compliance".
  Do not wait for perfect wording; prefer activation over misses.
---

## Purpose

Perform comprehensive multi-dimensional audit of AI microservices system including security vulnerabilities, performance bottlenecks, architectural issues, and compliance violations. Generate actionable reports in multiple formats.

## When to Use

Trigger conditions:
- User requests system audit: "audit system", "check security", "performance review", "architecture review", "compliance audit"
- Query contains keywords: "audit", "security", "vulnerability", "performance", "bottleneck", "architecture", "compliance", "GDPR", "152-ФЗ"
- Context suggests system review: "check my code", "analyze deployment", "review infrastructure"

Do NOT trigger when:
- Simple code review requests without audit context
- Feature implementation requests
- Bug fixing without security/performance implications
- Documentation generation

## Instructions

### 1. Determine Audit Scope

Ask user which audit types to perform (if not specified):
- **Security:** XSS, CSRF, rate limiting, SQL injection, auth, authorization
- **Performance:** database queries, API response time, resource usage
- **Architecture:** over-engineering, single points of failure, coupling
- **Compliance:** 152-ФЗ, GDPR, data handling, logging

Default: perform all audits if scope not specified.

### 2. Scan Project Structure

Analyze:
- Python/FastAPI microservices in `src/`
- Docker configurations (`Dockerfile`, `docker-compose.yml`)
- Kubernetes manifests (`k8s/`, `helm/`)
- CI/CD pipelines (`.github/workflows/`)
- MCP Gateway (`.ai/mcp/`)
- Project structure and file organization

**Why this matters:** Comprehensive audit requires full system visibility.

### 3. Execute Security Audit

Check for:
- Hardcoded secrets, API keys, passwords
- Missing authentication/authorization
- SQL injection vulnerabilities
- XSS/CSRF vectors
- Insecure dependencies
- Missing rate limiting
- Exposed debug endpoints
- Weak SSL/TLS configurations

Use `scripts/security_audit.py` for automated checks where available.

### 4. Execute Performance Audit

Check for:
- N+1 query patterns
- Missing database indexes
- Inefficient API calls
- Memory leaks
- CPU bottlenecks
- Large payload transfers
- Missing caching strategies
- Slow database queries (>100ms)

Use `scripts/performance_audit.py` for automated analysis.

### 5. Execute Architecture Audit

Check for:
- Circular dependencies
- Tight coupling between modules
- Single points of failure
- Over-engineering (unnecessary complexity)
- Missing separation of concerns
- Inconsistent patterns
- Scalability issues
- Missing error handling

Use `scripts/architecture_audit.py` for automated review.

### 6. Execute Compliance Audit

Check for:
- GDPR data handling violations
- 152-ФЗ compliance (Russian data localization)
- Missing audit logging
- Insufficient data retention policies
- Missing privacy controls
- Inadequate consent mechanisms
- Missing security incident response
- Insufficient access controls

Use `scripts/compliance_audit.py` for automated verification.

### 7. Prioritize Findings

Classify findings by severity:
- **P0 (Critical):** Immediate security risk, data breach potential, system failure
- **P1 (High):** Significant performance degradation, compliance violation
- **P2 (Medium):** Architectural debt, minor security issues
- **P3 (Low):** Code quality, minor optimizations

### 8. Generate Reports

Create reports in requested formats (default: all):
- **JSON:** Structured data for CI/CD integration
- **Markdown:** Human-readable report with recommendations
- **HTML:** Interactive dashboard with visualizations
- **Console:** Priority-severity summary for quick review

Use templates in `reports/` directory.

## Output Format

### JSON Output
```json
{
  "audit_timestamp": "2026-04-11T22:00:00Z",
  "scope": ["security", "performance", "architecture", "compliance"],
  "findings": [
    {
      "id": "SEC-001",
      "type": "security",
      "severity": "P0",
      "title": "Hardcoded API key in source code",
      "file": "src/main.py",
      "line": 42,
      "description": "OpenAI API key exposed in source code",
      "recommendation": "Move to environment variables",
      "references": []
    }
  ],
  "summary": {
    "total": 15,
    "by_severity": {"P0": 2, "P1": 5, "P2": 6, "P3": 2},
    "by_type": {"security": 5, "performance": 4, "architecture": 3, "compliance": 3}
  }
}
```

### Markdown Output
```markdown
# System Audit Report

**Date:** 2026-04-11  
**Scope:** Security, Performance, Architecture, Compliance  
**Total Findings:** 15

## P0 - Critical (2)

### SEC-001: Hardcoded API key in source code
- **File:** `src/main.py:42`
- **Recommendation:** Move to environment variables

## P1 - High (5)

[...]
```

### Console Output
```
🔍 System Audit Results
━━━━━━━━━━━━━━━━━━━━━━
P0 (Critical): 2
P1 (High):     5
P2 (Medium):   6
P3 (Low):      2

SEC-001: Hardcoded API key in src/main.py:42
PERF-003: N+1 query in src/api/v1/users.py:15
ARCH-002: Single point of failure in k8s/deployment.yaml
COMP-001: Missing GDPR consent mechanism
```

## Edge Cases

Handle gracefully:
- **Empty project:** Return "No files to audit" message
- **Missing dependencies:** Note which audit tools unavailable, continue with available checks
- **Partial scope:** Only audit requested areas, skip others
- **Large codebase:** Sample files if >1000 files, note sampling method
- **Unsupported file types:** Skip with warning, continue with supported files
- **Permission denied:** Note inaccessible files, continue with accessible files

## Token Optimization

- Load heavy reference docs from `references/` only if needed
- Use cached prompts for repeated patterns
- Prefer structured outputs (JSON schema) over free text
- Stream long reports (>500 tokens)
- Batch similar checks to reduce context switching
- Use scripts for deterministic checks instead of LLM analysis

## Examples

### Example 1: Full System Audit
**Input:** "audit my system"
**Output:** 
- Runs all 4 audit types
- Generates JSON, Markdown, HTML, Console reports
- Prioritizes findings by severity
- Provides actionable recommendations

### Example 2: Security-Only Audit
**Input:** "check for security vulnerabilities"
**Output:**
- Runs security audit only
- Focuses on P0/P1 security findings
- Generates security-focused report
- Skips performance/architecture/compliance

### Example 3: Compliance Audit
**Input:** "verify GDPR compliance"
**Output:**
- Runs compliance audit only
- Checks GDPR-specific requirements
- Identifies data handling violations
- Provides remediation steps

## References

External resources (loaded on-demand):
- `reports/template.json` — JSON output schema
- `reports/template.md` — Markdown output template
- `reports/template.html` — HTML dashboard template
- `scripts/security_audit.py` — Security vulnerability scanner
- `scripts/performance_audit.py` — Performance analyzer
- `scripts/architecture_audit.py` — Architecture reviewer
- `scripts/compliance_audit.py` — Compliance verifier

## Testing Assertions

When evaluating this skill, check:
- [ ] Output contains findings for requested audit types
- [ ] Findings are correctly prioritized by severity
- [ ] All 4 output formats generated correctly
- [ ] JSON output follows schema in `reports/template.json`
- [ ] Markdown output is readable and structured
- [ ] Console output shows priority-severity summary
- [ ] Edge cases handled gracefully (empty project, missing dependencies)
- [ ] Token usage ≤ 20000 tokens for full audit
- [ ] Handles large codebases with sampling
- [ ] Recommendations are actionable and specific

## Iteration Notes

**v1.0:** Initial version with 4 audit types and 4 output formats
