# Universal AI Rules Structure

## 📁 Project Structure

```
project-root/
├── .ai/                          # Universal rules location
│   ├── rules/                    # Shared rules (all IDEs)
│   │   ├── 000-core.mdc
│   │   ├── 001-agentic.mdc
│   │   ├── 002-api.mdc
│   │   └── README.md
│   ├── skills/                   # Skill Creator system
│   │   ├── SKILL_CREATOR.md
│   │   ├── SKILL_TEMPLATE.md
│   │   ├── agents/
│   │   │   ├── grader.md
│   │   │   ├── comparator.md
│   │   │   └── analyzer.md
│   │   └── schemas/
│   │       └── evals_schema.json
│   └── prompts/                  # Shared system prompts
│       └── agent_system.md
│
├── .cursor/                      # Cursor IDE specific
│   ├── rules/                    # Symlink → .ai/rules/
│   └── skills/                   # Symlink → .ai/skills/
│
├── .windsurf/                    # Windsurf specific
│   ├── rules/                    # Symlink → .ai/rules/
│   └── cascades/                 # Windsurf cascades (optional)
│
├── .idea/                        # PyCharm specific
│   ├── ai-rules.xml              # Config pointing to .ai/
│   └── fileTemplates/
│
└── src/
    └── ...
```

---

## 🔧 Setup for Each IDE

### **1. Cursor**

**Rules location:** `.cursor/rules/` or root-level `.mdc` files

**Setup:**
```bash
# Option A: Symlinks (recommended)
ln -s ../.ai/rules .cursor/rules
ln -s ../.ai/skills .cursor/skills

# Option B: Copy files to root
cp .ai/rules/*.mdc .
```

**Cursor Settings** (`.cursor/settings.json`):
```json
{
  "cursor.rules.directories": [".ai/rules", ".cursor/rules"],
  "cursor.skills.directories": [".ai/skills", ".cursor/skills"]
}
```

---

### **2. Windsurf**

**Rules location:** `.windsurf/rules/` or `.windsurfrules`

**Setup:**
```bash
# Option A: Symlinks
ln -s ../.ai/rules .windsurf/rules

# Option B: Single file (Windsurf supports .windsurfrules)
cat .ai/rules/*.mdc > .windsurfrules
```

**Windsurf Config** (`.windsurf/config.json`):
```json
{
  "ai": {
    "rulesPath": [".ai/rules", ".windsurf/rules"],
    "cascadesEnabled": true
  }
}
```

---

### **3. PyCharm (AI Assistant)**

**Rules location:** PyCharm AI doesn't use `.mdc` natively, needs workaround

**Setup:**

#### Option A: Custom File Watcher
`.idea/watcherTasks.xml`:
```xml
<TaskOptions>
  <option name="name" value="AI Rules Sync" />
  <option name="description" value="Convert .mdc to PyCharm format" />
  <option name="fileExtension" value="mdc" />
  <option name="program" value="$ProjectFileDir$/.ai/scripts/sync-pycharm.sh" />
  <option name="workingDir" value="$ProjectFileDir$" />
</TaskOptions>
```

#### Option B: Include in Docstrings/Comments
`.idea/ai-context.txt` (loaded via "Attach Context"):
```
# This file is auto-generated from .ai/rules/
# Last sync: 2024-01-15

<content from all .mdc files>
```

#### Option C: PyCharm AI Custom Instructions
Settings → Tools → AI Assistant → Custom Instructions:
```
Load rules from: ${PROJECT_DIR}/.ai/rules/

Apply token economy principles:
- Generate only diffs
- Use # ... existing ... for unchanged code
[paste core rules summary]
```

---

## 🔄 Automatic Sync Script

**`.ai/scripts/sync-all.sh`** — keeps all IDE configs in sync:

```bash
#!/bin/bash
set -e

AI_DIR=".ai/rules"
CURSOR_DIR=".cursor/rules"
WINDSURF_DIR=".windsurf/rules"
PYCHARM_CONTEXT=".idea/ai-context.txt"

echo "🔄 Syncing AI rules to all IDEs..."

# Cursor
if [ -d ".cursor" ]; then
  echo "  → Cursor"
  mkdir -p "$CURSOR_DIR"
  rsync -av --delete "$AI_DIR/" "$CURSOR_DIR/"
fi

# Windsurf
if [ -d ".windsurf" ]; then
  echo "  → Windsurf"
  mkdir -p "$WINDSURF_DIR"
  rsync -av --delete "$AI_DIR/" "$WINDSURF_DIR/"
  
  # Also create single .windsurfrules file
  cat "$AI_DIR"/*.mdc > .windsurfrules
fi

# PyCharm
if [ -d ".idea" ]; then
  echo "  → PyCharm"
  echo "# AI Rules Context - Auto-generated from .ai/rules/" > "$PYCHARM_CONTEXT"
  echo "# Last sync: $(date)" >> "$PYCHARM_CONTEXT"
  echo "" >> "$PYCHARM_CONTEXT"
  
  for file in "$AI_DIR"/*.mdc; do
    echo "## $(basename $file)" >> "$PYCHARM_CONTEXT"
    cat "$file" >> "$PYCHARM_CONTEXT"
    echo -e "\n---\n" >> "$PYCHARM_CONTEXT"
  done
fi

echo "✅ Sync complete!"
```

**Add to `.git/hooks/pre-commit`:**
```bash
#!/bin/bash
.ai/scripts/sync-all.sh
git add .cursor/ .windsurf/ .idea/ai-context.txt .windsurfrules
```

---

## 📋 Universal Rule Format

**Use extended frontmatter for IDE compatibility:**

```markdown
---
description: Core rules (all IDEs)
globs: ["**/*.py"]
alwaysApply: true

# IDE-specific metadata
cursor:
  priority: 1
  category: "core"
windsurf:
  cascade: true
pycharm:
  scope: "project"
---

# CORE RULES

[content compatible with all IDEs]
```

---

## 🎯 IDE-Specific Features

### Cursor-Only Features
```markdown
<!-- cursor:start -->
Use `cursor.ai` API for enhanced completions
<!-- cursor:end -->
```

### Windsurf-Only Features
```markdown
<!-- windsurf:cascade -->
This section flows to related files
<!-- windsurf:end -->
```

### PyCharm-Only Features
```markdown
<!-- pycharm:inspection -->
Suppress inspection: PEP8Naming
<!-- pycharm:end -->
```

---

## 🔍 Testing IDE Compatibility

**`.ai/scripts/test-compatibility.sh`:**
```bash
#!/bin/bash

echo "Testing rule compatibility..."

# Check Cursor
if command -v cursor &> /dev/null; then
  echo "✓ Cursor installed"
  # Test rule loading
fi

# Check Windsurf
if [ -d "$HOME/.windsurf" ]; then
  echo "✓ Windsurf installed"
fi

# Check PyCharm
if [ -d ".idea" ]; then
  echo "✓ PyCharm project detected"
  echo "  Note: Manually attach .idea/ai-context.txt in AI Assistant"
fi

echo -e "\n📁 Rules structure:"
tree -L 3 .ai/
```

---

## 📦 Distribution

**For team sharing:**

```bash
# Package for distribution
tar -czf ai-rules.tar.gz .ai/ .cursor/ .windsurf/ .windsurfrules

# Setup on new machine
tar -xzf ai-rules.tar.gz
.ai/scripts/sync-all.sh
```

**`.gitignore` entries:**
```
# Keep source in .ai/
# IDE-specific copies are generated

# But DO commit:
!.ai/
!.windsurfrules
!.idea/ai-context.txt
```

---

## 🚀 Quick Start

```bash
# 1. Clone/init project
cd your-project/

# 2. Copy .ai/ directory with rules
cp -r /path/to/ai-rules/.ai .

# 3. Run sync for your IDE(s)
.ai/scripts/sync-all.sh

# 4. IDE-specific setup:

# Cursor: restart, rules auto-load
# Windsurf: restart, check .windsurf/rules/
# PyCharm: attach .idea/ai-context.txt in AI Assistant settings
```

---

## ✅ Verification Checklist

- [ ] `.ai/rules/*.mdc` exist
- [ ] Cursor: `.cursor/rules/` populated or root `.mdc` files
- [ ] Windsurf: `.windsurf/rules/` or `.windsurfrules` exists
- [ ] PyCharm: `.idea/ai-context.txt` attached in AI Assistant
- [ ] Sync script executable: `chmod +x .ai/scripts/*.sh`
- [ ] Git hook configured (optional)
- [ ] Team members can `sync-all.sh` successfully

---

## 💡 Best Practices

1. **Single Source of Truth**: Always edit `.ai/rules/*.mdc`
2. **Sync Frequently**: Run `sync-all.sh` after rule changes
3. **IDE Fallback**: If IDE doesn't support rules, copy to project root
4. **Version Control**: Commit `.ai/` + generated IDE configs
5. **Documentation**: Keep `.ai/README.md` with setup instructions