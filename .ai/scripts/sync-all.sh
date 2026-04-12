#!/bin/bash
# Universal AI Rules Sync Script
# Syncs .ai/rules and .ai/skills to Cursor, Windsurf, PyCharm (.idea and .aiassistant)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directories
AI_DIR=".ai/rules"
SKILLS_DIR=".ai/skills"
CURSOR_DIR=".cursor"
WINDSURF_DIR=".windsurf"
PYCHARM_CONTEXT=".idea/ai-context.txt"
PYCHARM_RULES_DIR=".aiassistant/rules"

# Flags
FORCE_CURSOR=false
FORCE_WINDSURF=false
FORCE_PYCHARM=false
FORCE_AIASSISTANT=false
FORCE_ALL=false
USE_SYMLINKS=false
CHECK_SOT=false

for arg in "$@"; do
  case "$arg" in
    --force-cursor) FORCE_CURSOR=true ;;
    --force-windsurf) FORCE_WINDSURF=true ;;
    --force-pycharm) FORCE_PYCHARM=true ;;
    --force-aiassistant) FORCE_AIASSISTANT=true ;;
    --force-all) FORCE_ALL=true ;;
    --symlinks) USE_SYMLINKS=true ;;
    --check-sot) CHECK_SOT=true ;;
    *)
      echo -e "${YELLOW}Unknown flag: $arg${NC}"
      ;;
  esac
done

run_sot_check() {
  if command -v git &> /dev/null && git rev-parse --git-dir > /dev/null 2>&1; then
    ai_changed=$(git status --porcelain -- .ai/rules .ai/skills 2>/dev/null || true)
    mirrors_changed=$(git status --porcelain -- .cursor .windsurf .windsurfrules .idea/ai-context.txt .aiassistant/rules 2>/dev/null || true)

    if [ -n "$mirrors_changed" ] && [ -z "$ai_changed" ]; then
      echo -e "${RED}❌ SoT check failed: IDE mirrors changed without source changes in .ai/rules or .ai/skills${NC}"
      echo "Fix:"
      echo "  1) Edit only .ai/rules and .ai/skills"
      echo "  2) Re-run ./.ai/scripts/sync-all.sh"
      exit 2
    fi
    echo -e "${GREEN}✅ SoT check passed${NC}"
  else
    echo -e "${YELLOW}⚠️  SoT check skipped: not a git repository${NC}"
  fi
}

# Check-only mode for CI/pre-commit
if [ "$CHECK_SOT" = true ] && [ "$#" -eq 1 ]; then
  run_sot_check
  exit 0
fi

echo -e "${GREEN}🔄 Syncing AI rules to all IDEs...${NC}\n"

# Check if .ai/rules exists
if [ ! -d "$AI_DIR" ]; then
  echo -e "${RED}Error: $AI_DIR not found${NC}"
  echo "Run this script from project root with .ai/rules/ directory"
  exit 1
fi

# Function to sync directory
sync_dir() {
  local src=$1
  local dest=$2
  local ide_name=$3

  if [ -d "$(dirname $dest)" ] || [ "$4" == "force" ]; then
    echo -e "${YELLOW}  → $ide_name${NC}"
    mkdir -p "$dest"

    # Use rsync if available, fallback to cp
    if command -v rsync &> /dev/null; then
      rsync -av --delete "$src/" "$dest/" > /dev/null
    else
      rm -rf "$dest"
      cp -r "$src" "$dest"
    fi

    echo -e "${GREEN}    ✓ Synced $dest${NC}"
    return 0
  fi
  return 1
}

# 1. CURSOR
if [ -d ".cursor" ] || [ "$FORCE_CURSOR" = true ] || [ "$FORCE_ALL" = true ]; then
  sync_dir "$AI_DIR" "$CURSOR_DIR/rules" "Cursor (rules)"

  if [ -d "$SKILLS_DIR" ]; then
    sync_dir "$SKILLS_DIR" "$CURSOR_DIR/skills" "Cursor (skills)"
  fi
else
  echo -e "${YELLOW}  ⊘ Cursor not detected (no .cursor/)${NC}"
fi

# 2. WINDSURF
if [ -d ".windsurf" ] || [ "$FORCE_WINDSURF" = true ] || [ "$FORCE_ALL" = true ]; then
  sync_dir "$AI_DIR" "$WINDSURF_DIR/rules" "Windsurf (rules)"

  if [ -d "$SKILLS_DIR" ]; then
    sync_dir "$SKILLS_DIR" "$WINDSURF_DIR/skills" "Windsurf (skills)"
  fi

  # Create single .windsurfrules file
  echo -e "${YELLOW}  → Windsurf (.windsurfrules)${NC}"
  {
    echo "# Windsurf AI Rules - Auto-generated from .ai/rules/"
    echo "# Last sync: $(LC_ALL=C date)"
    echo ""

    for file in "$AI_DIR"/*.mdc; do
      if [ -f "$file" ]; then
        echo "# ================================================"
        echo "# $(basename $file)"
        echo "# ================================================"
        echo ""
        cat "$file"
        echo -e "\n"
      fi
    done
  } > .windsurfrules
  echo -e "${GREEN}    ✓ Created .windsurfrules${NC}"
else
  echo -e "${YELLOW}  ⊘ Windsurf not detected (no .windsurf/)${NC}"
fi

# 3. PYCHARM — .idea/ai-context.txt (legacy consolidated file)
if [ -d ".idea" ] || [ "$FORCE_PYCHARM" = true ] || [ "$FORCE_ALL" = true ]; then
  echo -e "${YELLOW}  → PyCharm (.idea/ai-context.txt)${NC}"

  # Create .idea if it doesn't exist
  mkdir -p .idea

  {
    echo "# PyCharm AI Assistant Context"
    echo "# Auto-generated from .ai/rules/"
    echo "# Last sync: $(LC_ALL=C date)"
    echo ""
    echo "==================================="
    echo "INSTRUCTIONS FOR AI ASSISTANT"
    echo "==================================="
    echo ""
    echo "These rules apply to ALL code generation in this project."
    echo "Read carefully and follow strictly."
    echo ""

    for file in "$AI_DIR"/*.mdc; do
      if [ -f "$file" ]; then
        echo ""
        echo "---------------------------------------------------"
        echo "FILE: $(basename $file)"
        echo "---------------------------------------------------"
        echo ""
        cat "$file"
        echo ""
      fi
    done

    # Add skills if present (recursive: SKILL.md from subdirs + *.md from root)
    if [ -d "$SKILLS_DIR" ]; then
      echo ""
      echo "==================================="
      echo "AVAILABLE SKILLS"
      echo "==================================="
      echo ""

      # Collect all skill files: root-level *.md and nested */SKILL.md
      skill_files=()
      while IFS= read -r -d '' f; do
        skill_files+=("$f")
      done < <(find "$SKILLS_DIR" -maxdepth 1 -name "*.md" -print0 2>/dev/null; find "$SKILLS_DIR" -mindepth 2 -name "SKILL.md" -print0 2>/dev/null; find "$SKILLS_DIR" -mindepth 2 -path "*/agents/*.md" -print0 2>/dev/null)

      # Sort and deduplicate
      IFS=$'\n' sorted_skills=($(sort -u <<<"${skill_files[*]}")); unset IFS

      for skill_file in "${sorted_skills[@]}"; do
        if [ -f "$skill_file" ]; then
          # Compute relative path for display
          rel_path="${skill_file#$SKILLS_DIR/}"
          echo ""
          echo "---------------------------------------------------"
          echo "SKILL: $rel_path"
          echo "---------------------------------------------------"
          echo ""
          cat "$skill_file"
          echo ""
        fi
      done
    fi
  } > "$PYCHARM_CONTEXT"

  echo -e "${GREEN}    ✓ Created $PYCHARM_CONTEXT${NC}"
else
  echo -e "${YELLOW}  ⊘ PyCharm not detected (no .idea/)${NC}"
fi

# 4. PYCHARM — .aiassistant/rules/ (official JetBrains format)
# Always sync when .idea exists or force flag is used
if [ -d ".idea" ] || [ -d ".aiassistant" ] || [ "$FORCE_PYCHARM" = true ] || [ "$FORCE_ALL" = true ] || [ "$FORCE_AIASSISTANT" = true ]; then
  echo -e "${YELLOW}  → PyCharm (.aiassistant/rules/)${NC}"

  mkdir -p "$PYCHARM_RULES_DIR"

  # Clean old generated files
  rm -f "$PYCHARM_RULES_DIR"/*.md 2>/dev/null || true

  synced_count=0

  # Copy rules: .mdc → .md
  for file in "$AI_DIR"/*.mdc; do
    if [ -f "$file" ]; then
      base_name=$(basename "$file" .mdc)
      dest_file="$PYCHARM_RULES_DIR/${base_name}.md"

      # Add header with rule type hint for PyCharm
      {
        echo "<!-- PyCharm AI Project Rule -->"
        echo "<!-- Source: $file -->"
        echo "<!-- Synced: $(LC_ALL=C date) -->"
        echo "<!-- Rule type: Always (apply to all files) -->"
        echo ""
        cat "$file"
      } > "$dest_file"

      echo -e "${GREEN}    ✓ ${base_name}.md${NC}"
      synced_count=$((synced_count + 1))
    fi
  done

  # Copy skills: flatten with prefixes to avoid name collisions
  if [ -d "$SKILLS_DIR" ]; then
    # Collect all skill files
    skill_files=()
    while IFS= read -r -d '' f; do
      skill_files+=("$f")
    done < <(find "$SKILLS_DIR" -maxdepth 1 -name "*.md" -print0 2>/dev/null; find "$SKILLS_DIR" -mindepth 2 -name "SKILL.md" -print0 2>/dev/null; find "$SKILLS_DIR" -mindepth 2 -path "*/agents/*.md" -print0 2>/dev/null)

    IFS=$'\n' sorted_skills=($(sort -u <<<"${skill_files[*]}")); unset IFS

    for skill_file in "${sorted_skills[@]}"; do
      if [ -f "$skill_file" ]; then
        rel_path="${skill_file#$SKILLS_DIR/}"
        # Create safe filename: replace / with -
        safe_name=$(echo "$rel_path" | sed 's|/|-|g')
        dest_file="$PYCHARM_RULES_DIR/skill-${safe_name}"

        {
          echo "<!-- PyCharm AI Skill Reference -->"
          echo "<!-- Source: $skill_file -->"
          echo "<!-- Synced: $(LC_ALL=C date) -->"
          echo "<!-- Rule type: Manually (trigger by name) -->"
          echo ""
          cat "$skill_file"
        } > "$dest_file"

        echo -e "${GREEN}    ✓ skill-${safe_name}${NC}"
        synced_count=$((synced_count + 1))
      fi
    done
  fi

  echo -e "${GREEN}    ✓ Total: $synced_count files in .aiassistant/rules/${NC}"
else
  echo -e "${YELLOW}  ⊘ PyCharm (.aiassistant) not detected (no .idea/ or .aiassistant/)${NC}"
fi

# 5. Create symlinks if requested
if [ "$USE_SYMLINKS" = true ]; then
  echo -e "\n${YELLOW}📎 Creating symlinks...${NC}"

  # Cursor symlinks
  if [ -d ".cursor" ]; then
    ln -sf "../$AI_DIR" "$CURSOR_DIR/rules" 2>/dev/null || true
    [ -d "$SKILLS_DIR" ] && ln -sf "../$SKILLS_DIR" "$CURSOR_DIR/skills" 2>/dev/null || true
    echo -e "${GREEN}  ✓ Cursor symlinks${NC}"
  fi

  # Windsurf symlinks
  if [ -d ".windsurf" ]; then
    ln -sf "../$AI_DIR" "$WINDSURF_DIR/rules" 2>/dev/null || true
    [ -d "$SKILLS_DIR" ] && ln -sf "../$SKILLS_DIR" "$WINDSURF_DIR/skills" 2>/dev/null || true
    echo -e "${GREEN}  ✓ Windsurf symlinks${NC}"
  fi
fi

# 6. Optional SoT check for CI/pre-commit usage
if [ "$CHECK_SOT" = true ]; then
  run_sot_check
fi

# Summary
echo -e "\n${GREEN}✅ Sync complete!${NC}\n"

# Show what was synced
echo "📋 Summary:"
[ -d "$CURSOR_DIR/rules" ] && echo "  • Cursor:      $CURSOR_DIR/rules/"
[ -f ".windsurfrules" ] && echo "  • Windsurf:    .windsurfrules"
[ -f "$PYCHARM_CONTEXT" ] && echo "  • PyCharm (legacy): $PYCHARM_CONTEXT"
[ -d "$PYCHARM_RULES_DIR" ] && echo "  • PyCharm (official): $PYCHARM_RULES_DIR/"

echo -e "\n💡 Usage tips:"
echo "  • Edit rules in $AI_DIR/ only"
echo "  • Run this script after changes: ./.ai/scripts/sync-all.sh"
echo "  • Use --symlinks flag to create symlinks instead of copies"
echo "  • Use --check-sot to fail when mirrors changed without .ai source changes"
echo "  • Force sync specific IDE: --force-cursor, --force-windsurf, --force-pycharm, --force-aiassistant"
echo "  • Force sync all IDEs (create if missing): --force-all"

# PyCharm setup instructions
if [ -d "$PYCHARM_RULES_DIR" ]; then
  echo -e "\n🔧 PyCharm setup:"
  echo "  1. Open Settings (Ctrl+Alt+S) → Tools → AI Assistant → Rules"
  echo "  2. The files in .aiassistant/rules/ are auto-detected"
  echo "  3. Set Rule type to 'Always' for rules, 'Manually' for skills"
fi

# Check for updates needed
if command -v git &> /dev/null && git rev-parse --git-dir > /dev/null 2>&1; then
  if git status --porcelain | grep -q "\.cursor/\|\.windsurf/\|\.windsurfrules\|ai-context.txt\|\.aiassistant/"; then
    echo -e "\n${YELLOW}⚠️  Changes detected. Consider committing:${NC}"
    echo "  git add .cursor/ .windsurf/ .windsurfrules .idea/ai-context.txt .aiassistant/"
    echo "  git commit -m 'sync: Update IDE AI rules'"
  fi
fi
