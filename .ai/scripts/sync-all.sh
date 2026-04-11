#!/bin/bash
# Universal AI Rules Sync Script
# Syncs .ai/rules to Cursor, Windsurf, and PyCharm

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
if [ -d ".cursor" ] || [ "$1" == "--force-cursor" ]; then
  sync_dir "$AI_DIR" "$CURSOR_DIR/rules" "Cursor (rules)"
  
  if [ -d "$SKILLS_DIR" ]; then
    sync_dir "$SKILLS_DIR" "$CURSOR_DIR/skills" "Cursor (skills)"
  fi
  
  # Also copy to root for global rules
  echo -e "${YELLOW}  → Cursor (root .mdc files)${NC}"
  cp "$AI_DIR"/*.mdc . 2>/dev/null || true
  echo -e "${GREEN}    ✓ Copied to root${NC}"
else
  echo -e "${YELLOW}  ⊘ Cursor not detected (no .cursor/)${NC}"
fi

# 2. WINDSURF
if [ -d ".windsurf" ] || [ "$1" == "--force-windsurf" ]; then
  sync_dir "$AI_DIR" "$WINDSURF_DIR/rules" "Windsurf (rules)"
  
  if [ -d "$SKILLS_DIR" ]; then
    sync_dir "$SKILLS_DIR" "$WINDSURF_DIR/skills" "Windsurf (skills)"
  fi
  
  # Create single .windsurfrules file
  echo -e "${YELLOW}  → Windsurf (.windsurfrules)${NC}"
  {
    echo "# Windsurf AI Rules - Auto-generated from .ai/rules/"
    echo "# Last sync: $(date)"
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

# 3. PYCHARM
if [ -d ".idea" ] || [ "$1" == "--force-pycharm" ] || [ "$1" == "--force-all" ]; then
  echo -e "${YELLOW}  → PyCharm (AI context)${NC}"
  
  # Create .idea if it doesn't exist
  mkdir -p .idea
  
  {
    echo "# PyCharm AI Assistant Context"
    echo "# Auto-generated from .ai/rules/"
    echo "# Last sync: $(date)"
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
    
    # Add skills if present
    if [ -d "$SKILLS_DIR" ]; then
      echo ""
      echo "==================================="
      echo "AVAILABLE SKILLS"
      echo "==================================="
      echo ""
      
      for skill_file in "$SKILLS_DIR"/*.md; do
        if [ -f "$skill_file" ]; then
          echo ""
          echo "---------------------------------------------------"
          echo "SKILL: $(basename $skill_file)"
          echo "---------------------------------------------------"
          echo ""
          cat "$skill_file"
          echo ""
        fi
      done
    fi
  } > "$PYCHARM_CONTEXT"
  
  echo -e "${GREEN}    ✓ Created $PYCHARM_CONTEXT${NC}"
  echo -e "${YELLOW}    ℹ Manual step: Attach this file in PyCharm AI Assistant settings${NC}"
else
  echo -e "${YELLOW}  ⊘ PyCharm not detected (no .idea/)${NC}"
fi

# 4. Create symlinks if requested
if [ "$1" == "--symlinks" ]; then
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

# Summary
echo -e "\n${GREEN}✅ Sync complete!${NC}\n"

# Show what was synced
echo "📋 Summary:"
[ -d "$CURSOR_DIR/rules" ] && echo "  • Cursor:    $CURSOR_DIR/rules/"
[ -f ".windsurfrules" ] && echo "  • Windsurf:  .windsurfrules"
[ -f "$PYCHARM_CONTEXT" ] && echo "  • PyCharm:   $PYCHARM_CONTEXT"

echo -e "\n💡 Usage tips:"
echo "  • Edit rules in $AI_DIR/ only"
echo "  • Run this script after changes: ./.ai/scripts/sync-all.sh"
echo "  • Use --symlinks flag to create symlinks instead of copies"
echo "  • Force sync specific IDE: --force-cursor, --force-windsurf, --force-pycharm"
echo "  • Force sync all IDEs (create if missing): --force-all"

# Check for updates needed
if command -v git &> /dev/null && git rev-parse --git-dir > /dev/null 2>&1; then
  if git status --porcelain | grep -q "\.cursor/\|\.windsurf/\|\.windsurfrules\|ai-context.txt"; then
    echo -e "\n${YELLOW}⚠️  Changes detected. Consider committing:${NC}"
    echo "  git add .cursor/ .windsurf/ .windsurfrules .idea/ai-context.txt"
    echo "  git commit -m 'sync: Update IDE AI rules'"
  fi
fi