# AI Skill System — Complete Guide

## What it is

AI Skill System is a cross-IDE platform for managing rules and skills for AI-assisted development. The system provides unified behavior for AI assistants (Cursor, Windsurf, PyCharm) through centralized rules, automatic synchronization, and a framework for creating/testing skills.

## Architecture

### Core Components

```
ai-skill-system/
├── .ai/                          # Source of Truth
│   ├── rules/                     # Universal rules (*.mdc)
│   │   ├── 000-core.mdc          # Core rules (token economy)
│   │   ├── 001-agentic.mdc       # Agentic systems
│   │   ├── 002-docker.mdc        # Docker standards
│   │   ├── 003-team-protocol.mdc # Team protocol
│   │   ├── 004-k8s.mdc           # Kubernetes standards
│   │   ├── 005-cicd.mdc          # CI/CD standards
│   │   └── 006-api.mdc           # API standards
│   ├── skills/                    # Skill Creator System
│   │   ├── SKILL_CREATOR.md      # Agent for creating skills
│   │   ├── SKILL_TEMPLATE.md     # Template for skills
│   │   ├── agents/               # Eval agents
│   │   │   ├── analyzer.md       # Result analysis
│   │   │   ├── comparator.md     # Iteration comparison
│   │   │   └── grader.md        # Assertion grading
│   │   ├── assertions/            # Programmatic checks
│   │   │   ├── check_json.py     # JSON validation
│   │   │   ├── check_format.py   # Format validation
│   │   │   └── README.md
│   │   └── schemas/               # JSON schemas for eval
│   │       └── eval_schema.json
│   ├── scripts/                   # Automation
│   │   ├── sync-all.sh           # IDE synchronization
│   │   ├── install-hooks.sh      # Git hooks
│   │   ├── aggregate_benchmark.py # Benchmark aggregation
│   │   ├── run_eval.py           # Eval execution
│   │   ├── migrate-field-names.sh # Field migration
│   │   └── start-mcp-gateway.sh  # Start MCP Gateway
│   ├── mcp/                       # MCP Gateway
│   │   ├── gateway.py            # FastAPI server
│   │   ├── config.json           # Service configuration
│   │   └── services/             # MCP service adapters
│   │       ├── __init__.py       # Adapter interface
│   │       └── filesystem.py     # Filesystem adapter
│   └── prompts/                   # System prompts
├── .cursor/                      # Cursor IDE configuration (auto-generated)
├── .windsurf/                    # Windsurf IDE configuration (auto-generated)
├── .windsurfrules                # Windsurf single rules file (auto-generated)
├── .idea/                        # PyCharm IDE configuration (legacy)
│   └── ai-context.txt            # Consolidated rules+skills (auto-generated)
├── .aiassistant/                 # PyCharm official rules (auto-generated)
│   └── rules/                    # Individual .md files for AI Assistant Rules
│       ├── 000-core.md           # Core rules (Rule type: Always)
│       ├── 001-agentic.md        # Agentic systems (Rule type: By file patterns)
│       ├── ...                   # Other rules
│       ├── skill-SKILL_CREATOR.md  # Skill creation (Rule type: Manually)
│       └── skill-system-*.md     # Other skills (Rule type: Manually)
├── evals/                        # Evaluation workspace
│   └── workspace/                # Structure for iterations
│       ├── iteration-1/
│       ├── iteration-2/
│       └── template/
├── TEAM.md                       # Team protocol (organizational layer)
└── SYSTEM_GUIDE.md               # This file
```

### How it works

#### 1. Rules (.mdc files)

`.mdc` (Markdown Config) files contain rules for AI assistants with metadata:

```yaml
---
description: Core rules for AI microservices
globs: ["**/*.py", "**/*.yaml"]
alwaysApply: true
---

# CORE — AI Microservices
## Token Economy
- Answer ONLY the question asked
- Generate ONLY diff/changed blocks
```

**Key fields:**
- `description` - rule description for triggering
- `globs` - which files to apply the rule to
- `alwaysApply` - whether to always apply

#### 2. IDE Synchronization

The `sync-all.sh` script copies rules from `.ai/rules/` to IDE-specific directories:

- **Cursor** → `.cursor/rules/`
- **Windsurf** → `.windsurf/rules/` + `.windsurfrules` (single file)
- **PyCharm (legacy)** → `.idea/ai-context.txt` (consolidated text file)
- **PyCharm (official)** → `.aiassistant/rules/` (individual `.md` files)

**Automation:** Git pre-commit hook automatically runs `sync-all.sh` before each commit.

#### 2.1 Single Source of Truth (SoT) for rules and skills

To reduce duplication, treat only these directories as canonical:

- `.ai/rules/` — canonical rules
- `.ai/skills/` — canonical skills

All other IDE-specific artifacts (`.cursor/`, `.windsurf/`, `.windsurfrules`, `.idea/ai-context.txt`, `.aiassistant/rules/`) are generated mirrors and must not be edited manually.

**Recommended options (MVP):**

1. **Copy-based sync (default, safest)**
   - Command: `./.ai/scripts/sync-all.sh`
   - Pros: works everywhere (Linux/macOS/Windows/GitHub)
   - Cons: duplicate files in repo

2. **Symlink-based mirrors (minimal duplication)**
   - Command: `./.ai/scripts/sync-all.sh --symlinks`
   - Pros: almost no physical duplication for Cursor/Windsurf folders
   - Cons: symlink behavior differs on Windows and some CI/archive flows

3. **Hybrid (recommended for current MVP)**
   - Keep copy-based sync as baseline for compatibility
   - Enable symlinks only in local dev environments where stable
   - Keep `.aiassistant/rules/` and `.windsurfrules` generated (they require transformed formats)

**Decision rule:** edit only `.ai/*`, regenerate mirrors via script, and enforce this in PR checks.

**Enforcement command (CI/pre-commit):**

```bash
./.ai/scripts/sync-all.sh --check-sot
```

This check fails if mirror files changed without corresponding changes in `.ai/rules/` or `.ai/skills/`.

#### 3. Skill Creator System

**Skill creation workflow:**

1. **Discovery** — gathering requirements (what the skill does, when it triggers)
2. **Requirements** — deep dive into edge cases, formats, success criteria
3. **SKILL.md** — creating skill file with "pushy" description
4. **Test Generation** — generating test cases
5. **Benchmarking** — running eval with assertions
6. **Optimization** — iterative description improvement

**Programmatic Assertions:**
- `check_json.py` — JSON validation
- `check_format.py` — format validation (json/markdown/yaml)
- Faster than LLM grading, deterministic, reusable

**Evaluation Workspace:**
```
workspace/iteration-1/
├── runs/
│   ├── test-1-with-skill/
│   │   ├── output.txt
│   │   └── metadata.json
│   └── test-1-baseline/
├── grading.json      # Per-test results
└── benchmark.json    # Aggregated metrics
```

#### 4. Team Protocol

**Roles:**
- **Arbitr (Ivan)** — final decision-maker
- **Vasya** — Principal Software Engineer (Front)
- **Yosya** — Principal AI/ML Engineer (Backend)
- **Bosya** — Principal GeoOps / MlOps / DevOps Engineer
- **Manya** — Principal UX/UI + Marketing Strategist
- **Sanya** — Behavioral Linguistics Expert
- **Kirill** — Security & Performance Auditor

**Workflow:**
1. Proposal (options + risks)
2. Arbitr approval (YES/NO/YES with constraints)
3. Implementation in small steps
4. Checkpoint + approval after each step
5. File creation only with explicit approval

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/semernyakov/ai-skill-system.git
cd ai-skill-system

# Install git hooks (auto-synchronization)
./.ai/scripts/install-hooks.sh

# Initial synchronization
./.ai/scripts/sync-all.sh
```

### Usage

#### For Cursor

Rules automatically load from `.cursor/rules/` when opening the project.

#### For Windsurf

Rules load from `.windsurf/rules/` or `.windsurfrules`.

#### For PyCharm

**Recommended method (official — PyCharm 2025.2+):**

Rules and skills are synced to `.aiassistant/rules/` as individual `.md` files.

1. Open **Settings** (`Ctrl+Alt+S`) → **Tools** → **AI Assistant** → **Rules**
2. Files in `.aiassistant/rules/` are auto-detected
3. For each rule file, set **Rule type**:
   - **Always** — for core rules (000-core.md, 003-team-protocol.md)
   - **Manually** — for skills (skill-*.md files)
   - **By file patterns** — for domain-specific rules (docker, k8s, api, etc.)

**Alternative method (legacy):**

1. Settings → Tools → AI Assistant → Rules
2. Click **New Project Rules File**
3. Select `.idea/ai-context.txt`
4. Set Rule type to **Always**

### MCP Gateway

MCP Gateway — centralized entry point for MCP services.

#### Start Gateway

```bash
# Install dependencies
pip install fastapi uvicorn pydantic

# Start gateway
./.ai/scripts/start-mcp-gateway.sh
```

Gateway will be available at `http://localhost:8080`

#### Available Services

**Filesystem Service:**
- `POST /mcp/filesystem/invoke` — file operations
  - `read_file` — read file
  - `write_file` — write file
  - `list_dir` — list directory
  - `delete_file` — delete file

**API Endpoints:**
- `GET /mcp/services` — list of services
- `GET /mcp/health/{service_name}` — health check
- `GET /mcp/{service_name}/capabilities` — service capabilities

See `MCP_GATEWAY.md` for more details

### Editing Rules

**IMPORTANT:** Edit only files in `.ai/rules/`!

After changes:

```bash
# Synchronize with IDE
./.ai/scripts/sync-all.sh

# Git add and commit (hook will automatically run sync)
git add .
git commit -m "Update rules"
```

### Creating a new skill

```bash
# Use SKILL_CREATOR.md as a guide
# Create SKILL.md in your project directory
```

### Running evaluation

```bash
# Prepare workspace
mkdir -p evals/workspace/iteration-1/runs

# Run eval
python .ai/scripts/run_eval.py evals.json evals/workspace/iteration-1

# Aggregate benchmarks
python .ai/scripts/aggregate_benchmark.py evals/workspace/iteration-1 --skill-name my-skill
```

## Key Concepts

### Token Economy

- Answer ONLY the question asked
- Generate ONLY diff/changed blocks
- Use `# ... existing ...` for unchanged code
- Skip docstrings except for public API
- Inline comments only for non-obvious logic

### Pushy Descriptions

Skill descriptions should be assertive, not passive:

**Bad:**
```yaml
description: How to build a simple fast dashboard
```

**Good:**
```yaml
description: >
  How to build a simple fast dashboard to display data.
  Use this skill whenever the user mentions dashboards, 
  data visualization, internal metrics, or wants to display 
  any kind of company data, even if they don't explicitly 
  ask for a 'dashboard.'
```

### Field Naming (Assertion Results)

Use exact field names for compatibility with viewer:

```json
{
  "text": "Output is valid JSON",
  "passed": true,
  "evidence": "Parsed 5 keys successfully"
}
```

## Troubleshooting

### Rules not synchronizing

```bash
# Manual synchronization
./.ai/scripts/sync-all.sh

# Check .ai/ directory
ls -la .ai/
```

### Git hooks not working

```bash
# Reinstall hooks
./.ai/scripts/install-hooks.sh

# Check hook file
cat .git/hooks/pre-commit
```

### Evaluation not running

```bash
# Check Python dependencies
python3 --version

# Check eval schema
python3 -m json.tool .ai/skills/schemas/eval_schema.json
```

### Markdown linting not working

Markdown linting is configured in `.pre-commit-config.yaml` (markdownlint), but not active due to missing dependencies.

**To activate, one of the following options is required:**

**Option A:** Install pre-commit framework
```bash
pip install pre-commit
pre-commit install
```

**Option B:** Install markdownlint-cli via bun
```bash
# Install dependencies
bun install

# Run markdown lint
bun run lint:md
```

Without installing these dependencies, markdown linting will not work. Configuration is ready but requires at least one dependency to activate.

## Additional Resources

- **TEAM.md** — Team protocol and roles
- **CONTRIBUTING.md** — Contributor guidelines
- **CODE_OF_CONDUCT.md** — Code of conduct
- **SECURITY.md** — Security policy
- **SUPPORT.md** — Support and FAQ
- **DISCLAIMER.md** — Disclaimer
- **CHANGELOG.md** — Change history

## License

MIT License — see LICENSE.md

## Contact

- Email: i.s.semernyakov@yandex.ru
- GitHub: https://github.com/semernyakov/ai-skill-system
