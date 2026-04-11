#!/usr/bin/env bash
set -euo pipefail

# Migrate assertion result field name from claim -> text
find . -type f \( -name '*.json' -o -name '*.md' \) \
  -not -path '*/.git/*' \
  -exec sed -i 's/"claim"\s*:/"text":/g' {} +

echo "Migration complete: claim -> text"
