#!/usr/bin/env bash
# Build script for PyPI

set -euo pipefail

echo "🏗️ Building AI Toolkit..."

# Очистка
rm -rf dist/ build/ *.egg-info/

# Сборка
python -m build

# Проверка
python -m twine check dist/*

echo "✅ Build complete!"
echo ""
echo "Files:"
ls -la dist/
echo ""
echo "To upload to PyPI:"
echo "  python -m twine upload dist/*"
echo ""
echo "To upload to TestPyPI:"
echo "  python -m twine upload --repository testpypi dist/*"

