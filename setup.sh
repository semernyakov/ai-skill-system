#!/bin/bash
# Universal AI Rules Setup Script
# Initializes .ai/ structure and IDE configs

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║   Universal AI Rules Setup             ║"
echo "║   Cursor • Windsurf • PyCharm          ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}\n"

# Detect current directory
if [ ! -f "pyproject.toml" ] && [ ! -f "setup.py" ] && [ ! -f "package.json" ]; then
  echo -e "${YELLOW}⚠️  No project files detected. Continue anyway? [y/N]${NC}"
  read -r response
  if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
  fi
fi

# Create .ai/ structure
echo -e "${GREEN}📁 Creating .ai/ structure...${NC}"

mkdir -p .ai/{rules,skills,prompts,scripts}
mkdir -p .ai/skills/{agents,schemas,examples}

# Create README
cat > .ai/README.md << 'EOF'
# AI Rules & Skills

Universal AI configuration for Cursor, Windsurf, and PyCharm.

## Structure

```
.ai/
├── rules/          # Core rules (*.mdc files)
├── skills/         # Skill Creator system
├── prompts/        # System prompts for agents
└── scripts/        # Automation scripts
```

## Setup

```bash
# Initial setup
./ai/scripts/setup.sh

# Sync to all IDEs
.ai/scripts/sync-all.sh

# Auto-sync on git commits
.ai/scripts/install-hooks.sh
```

## IDE-Specific Instructions

### Cursor
Rules auto-load from `.cursor/rules/` or root `*.mdc` files.

### Windsurf  
Rules load from `.windsurf/rules/` or `.windsurfrules` file.

### PyCharm
1. Open Settings → Tools → AI Assistant
2. Under "Custom Instructions", click "Attach Context"
3. Select `.idea/ai-context.txt`

## Editing Rules

**Always edit files in `.ai/rules/` only!**

Other locations are auto-generated. Run `sync-all.sh` after changes.
EOF

echo -e "${GREEN}  ✓ Created .ai/README.md${NC}"

# Create .gitignore for .ai/
cat > .ai/.gitignore << 'EOF'
# Ignore generated/temp files
*.pyc
__pycache__/
.DS_Store

# Keep structure
!rules/
!skills/
!prompts/
!scripts/
EOF

# Detect which IDEs are present
IDES_FOUND=()

if command -v cursor &> /dev/null || [ -d "$HOME/.cursor" ]; then
  IDES_FOUND+=("cursor")
  mkdir -p .cursor/{rules,skills}
  echo -e "${GREEN}  ✓ Detected Cursor${NC}"
fi

if [ -d "$HOME/.windsurf" ] || command -v windsurf &> /dev/null; then
  IDES_FOUND+=("windsurf")
  mkdir -p .windsurf/{rules,skills}
  echo -e "${GREEN}  ✓ Detected Windsurf${NC}"
fi

if [ -d ".idea" ]; then
  IDES_FOUND+=("pycharm")
  echo -e "${GREEN}  ✓ Detected PyCharm${NC}"
else
  # Create .idea for PyCharm compatibility
  mkdir -p .idea
  echo -e "${YELLOW}  ℹ Created .idea/ for PyCharm compatibility${NC}"
  IDES_FOUND+=("pycharm")
fi

if [ ${#IDES_FOUND[@]} -eq 0 ]; then
  echo -e "${YELLOW}  ⚠️  No IDEs detected, creating configs anyway${NC}"
  mkdir -p .cursor/{rules,skills}
  mkdir -p .windsurf/{rules,skills}
  mkdir -p .idea
fi

# Create sync script
cat > .ai/scripts/sync-all.sh << 'SYNCEOF'
#!/bin/bash
# See artifacts for full script content
# This is a placeholder - copy from sync-all.sh artifact
echo "Error: Replace this with actual sync-all.sh content"
exit 1
SYNCEOF

chmod +x .ai/scripts/sync-all.sh

# Create git hook installer
cat > .ai/scripts/install-hooks.sh << 'EOF'
#!/bin/bash
# Install git hooks for auto-sync

set -e

HOOK_FILE=".git/hooks/pre-commit"

if [ ! -d ".git" ]; then
  echo "Error: Not a git repository"
  exit 1
fi

mkdir -p .git/hooks

# Create or append to pre-commit hook
if [ -f "$HOOK_FILE" ]; then
  echo "Appending to existing pre-commit hook..."
  echo "" >> "$HOOK_FILE"
  echo "# Auto-sync AI rules" >> "$HOOK_FILE"
else
  echo "Creating new pre-commit hook..."
  echo "#!/bin/bash" > "$HOOK_FILE"
fi

cat >> "$HOOK_FILE" << 'HOOK'

# Sync AI rules before commit
if [ -f ".ai/scripts/sync-all.sh" ]; then
  echo "🔄 Syncing AI rules..."
  .ai/scripts/sync-all.sh
  
  # Stage generated files
  git add .cursor/ .windsurf/ .windsurfrules .idea/ai-context.txt 2>/dev/null || true
fi
HOOK

chmod +x "$HOOK_FILE"

echo "✅ Git hook installed: $HOOK_FILE"
echo "AI rules will auto-sync before each commit"
EOF

chmod +x .ai/scripts/install-hooks.sh

# Update .gitignore
if [ -f ".gitignore" ]; then
  if ! grep -q ".ai/" .gitignore 2>/dev/null; then
    echo "" >> .gitignore
    echo "# AI Rules - keep source, ignore IDE copies" >> .gitignore
    echo "# (sync-all.sh regenerates these)" >> .gitignore
    echo "# !.ai/" >> .gitignore
    echo "# !.windsurfrules" >> .gitignore
    echo "# !.idea/ai-context.txt" >> .gitignore
  fi
fi

# Summary
echo -e "\n${GREEN}✅ Setup complete!${NC}\n"

echo "📋 Next steps:"
echo ""
echo "1. Add your rules to .ai/rules/"
echo "   Example: .ai/rules/000-core.mdc"
echo ""
echo "2. Sync to IDEs:"
echo "   ${BLUE}.ai/scripts/sync-all.sh${NC}"
echo ""
echo "3. (Optional) Install git hooks for auto-sync:"
echo "   ${BLUE}.ai/scripts/install-hooks.sh${NC}"
echo ""

if [[ " ${IDES_FOUND[@]} " =~ " pycharm " ]]; then
  echo "4. PyCharm users: Attach context file"
  echo "   Settings → Tools → AI Assistant → Custom Instructions"
  echo "   → Attach: .idea/ai-context.txt"
  echo ""
fi

echo "📚 Documentation: .ai/README.md"
echo ""

# Offer to download example rules
echo -e "${YELLOW}Download example rules? [y/N]${NC}"
read -r download_examples

if [[ "$download_examples" =~ ^[Yy]$ ]]; then
  echo "Creating example rules..."
  
  # Create minimal example
  cat > .ai/rules/000-core.mdc << 'RULEEOF'
---
description: Core rules for this project
globs: ["**/*.py"]
alwaysApply: true
---

# CORE RULES

## Token Economy
- Answer ONLY what is asked
- Generate ONLY changed code blocks
- Use `# ... existing ...` for unchanged sections
- Skip docstrings on private methods

## Python Standards
- Python 3.11+
- Type hints everywhere
- Async-first for I/O operations
- Pydantic v2 for models
RULEEOF

  echo -e "${GREEN}  ✓ Created .ai/rules/000-core.mdc${NC}"
  echo -e "${YELLOW}  ℹ Add more rules based on your needs${NC}"
fi

echo -e "\n${GREEN}🚀 Ready to use!${NC}"