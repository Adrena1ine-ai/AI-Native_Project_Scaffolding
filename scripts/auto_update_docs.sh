#!/bin/bash
# Auto-update PROJECT_STATUS.md and CURRENT_CONTEXT_MAP.md for AI Toolkit
# This script should be run after any changes to the AI Toolkit codebase

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "📊 Auto-updating project documentation..."

# Update PROJECT_STATUS.md
if [ -f "src/utils/status_generator.py" ]; then
    echo "  → Updating PROJECT_STATUS.md..."
    python3 -m src.cli status . --skip-tests 2>/dev/null || python -m src.cli status . --skip-tests 2>/dev/null
    echo "  ✅ PROJECT_STATUS.md updated"
else
    echo "  ⚠️  status_generator.py not found"
fi

# Update CURRENT_CONTEXT_MAP.md
if [ -f "generate_map.py" ]; then
    echo "  → Updating CURRENT_CONTEXT_MAP.md..."
    python3 generate_map.py 2>/dev/null || python generate_map.py 2>/dev/null
    echo "  ✅ CURRENT_CONTEXT_MAP.md updated"
elif [ -f "src/utils/context_map.py" ]; then
    echo "  → Updating CURRENT_CONTEXT_MAP.md (via module)..."
    python3 -c "from src.utils.context_map import write_context_map; from pathlib import Path; write_context_map(Path('.'), 'CURRENT_CONTEXT_MAP.md')" 2>/dev/null
    echo "  ✅ CURRENT_CONTEXT_MAP.md updated"
else
    echo "  ⚠️  Context map generator not found"
fi

echo "✅ Documentation auto-update complete"

