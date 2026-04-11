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
