#!/bin/bash
#
# AI-Native Project Scaffolding — Quick Start Script (Linux/macOS)
# 
# Usage:
#   ./start.sh
#   ./start.sh --port 3000
#   ./start.sh --no-browser
#

set -e

# Default values
PORT=8080
OPEN_BROWSER=true

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --port|-p)
            PORT="$2"
            shift 2
            ;;
        --no-browser)
            OPEN_BROWSER=false
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Header
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  🛠️  AI-Native Project Scaffolding                       ║${NC}"
echo -e "${CYAN}║  Quick Start Script for Linux/macOS                      ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check Python
echo -e "${YELLOW}🔍 Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo -e "${RED}   ❌ Python not found! Please install Python 3.10+${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON --version 2>&1)
echo -e "${GREEN}   ✅ $PYTHON_VERSION${NC}"

# Check version
MAJOR=$($PYTHON -c "import sys; print(sys.version_info.major)")
MINOR=$($PYTHON -c "import sys; print(sys.version_info.minor)")
if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]); then
    echo -e "${RED}   ❌ Python 3.10+ required, found $MAJOR.$MINOR${NC}"
    exit 1
fi

# Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
$PYTHON -m pip install -q pyyaml fastapi uvicorn jinja2 python-multipart 2>/dev/null || true
echo -e "${GREEN}   ✅ Dependencies installed${NC}"

# Check if port is available
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}   ⚠️  Port $PORT is in use, trying $((PORT + 1))...${NC}"
    PORT=$((PORT + 1))
fi

# Start Dashboard
echo ""
echo -e "${GREEN}🚀 Starting Dashboard on http://127.0.0.1:$PORT ...${NC}"
echo ""

# Open browser
if [ "$OPEN_BROWSER" = true ]; then
    if command -v xdg-open &> /dev/null; then
        xdg-open "http://127.0.0.1:$PORT" &
    elif command -v open &> /dev/null; then
        open "http://127.0.0.1:$PORT" &
    fi
fi

# Run
$PYTHON -m web.app --port $PORT --no-browser

