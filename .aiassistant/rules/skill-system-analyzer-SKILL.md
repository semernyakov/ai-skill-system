<!-- PyCharm AI Skill Reference -->
<!-- Source: .ai/skills/system-analyzer/SKILL.md -->
<!-- Synced: Sun Apr 12 22:59:25 MSK 2026 -->
<!-- Rule type: Manually (trigger by name) -->

---
name: system-analyzer
description: >
  Analyzes the entire codebase and outputs system statistics.
  Trigger on: "analyze system", "codebase stats", "project metrics",
  "show statistics", "analyze architecture", "system overview".
  Generates: file counts, LOC, language distribution, dependency analysis.
---

# System Analyzer

## Instructions

1. **Discover structure**
   - List all directories recursively
   - Identify project roots (where package.json, pyproject.toml, go.mod exist)
   - Skip: node_modules/, .venv/, __pycache__/, .git/, build/, dist/

2. **Collect metrics**
   - File count by extension
   - Lines of code (excluding blank lines and comments)
   - Language distribution (percentage)
   - Directory depth and nesting level

3. **Analyze dependencies**
   - Parse package.json, requirements.txt, Cargo.toml, go.mod
   - Count direct dependencies
   - Identify outdated or vulnerable (if lock files present)

4. **Output format**
   - Use JSON for machine-readable output
   - Include human-readable summary above JSON

## Output Format

```markdown
## System Analysis: {project_name}

**Overview:** {brief description}
- Total files: {N}
- Total LOC: {N}
- Languages: {list}

```json
{
  "project_name": "...",
  "scan_timestamp": "ISO8601",
  "summary": {
    "total_files": 0,
    "total_loc": 0,
    "languages": [
      {"name": "Python", "files": 0, "loc": 0, "percentage": 0.0}
    ]
  },
  "structure": {
    "max_depth": 0,
    "root_dirs": [],
    "package_managers": ["pip", "npm"]
  },
  "dependencies": {
    "direct": 0,
    "dev": 0,
    "outdated": 0
  }
}
```
```

## Edge Cases

- **Empty directories**: Skip, don't count
- **Binary files**: Count in file stats, exclude from LOC
- **No package manager**: deps = null, not error
- **Symlinks**: Follow once, detect cycles, count target once
- **Huge files (>1MB)**: Read first 1000 lines only, add flag `[partial]`
- **Permission denied**: Log skip, continue scan
- **Mixed languages**: Group by extension, sort by LOC descending
