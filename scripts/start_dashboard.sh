#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 🌐 AI Toolkit — Start Web Dashboard
# ═══════════════════════════════════════════════════════════

set -e

cd "$(dirname "$0")/.."

echo "🌐 Starting AI Toolkit Dashboard..."
echo ""

# Check dependencies
if ! python3 -c "import fastapi, uvicorn, jinja2" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install fastapi uvicorn jinja2
fi

# Start server
python3 -m web.app

