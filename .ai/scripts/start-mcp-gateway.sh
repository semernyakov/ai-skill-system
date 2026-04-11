#!/bin/bash
# Start MCP Gateway Server

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

MCP_DIR=".ai/mcp"
GATEWAY_SCRIPT="$MCP_DIR/gateway.py"

# Check if gateway script exists
if [ ! -f "$GATEWAY_SCRIPT" ]; then
  echo "Error: $GATEWAY_SCRIPT not found"
  exit 1
fi

echo -e "${GREEN}🚀 Starting MCP Gateway...${NC}"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
  echo "Error: python3 not found"
  exit 1
fi

# Check if FastAPI and uvicorn are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
  echo -e "${YELLOW}⚠️  FastAPI not installed. Installing...${NC}"
  pip install fastapi uvicorn
fi

# Start the gateway
cd "$(dirname "$0")/.." || exit 1
python3 "$GATEWAY_SCRIPT"
