#!/usr/bin/env bash
# Publish to PyPI

set -euo pipefail

# Проверяем что мы не забыли обновить версию
VERSION=$(grep 'version = ' pyproject.toml | head -1 | cut -d'"' -f2)
echo "📦 Publishing AI Toolkit v$VERSION"

# Проверяем что тесты проходят
echo "🧪 Running tests..."
pytest tests/ -v --tb=short

# Сборка
echo "🏗️ Building..."
rm -rf dist/ build/ *.egg-info/
python -m build

# Проверка
echo "🔍 Checking..."
python -m twine check dist/*

# Подтверждение
read -p "Upload to PyPI? (y/N): " confirm
if [ "$confirm" != "y" ]; then
    echo "❌ Cancelled"
    exit 0
fi

# Публикация
echo "🚀 Uploading to PyPI..."
python -m twine upload dist/*

echo "✅ Published!"
echo ""
echo "Install with:"
echo "  pip install ai-toolkit==$VERSION"


# Publish to PyPI

set -euo pipefail

# Проверяем что мы не забыли обновить версию
VERSION=$(grep 'version = ' pyproject.toml | head -1 | cut -d'"' -f2)
echo "📦 Publishing AI Toolkit v$VERSION"

# Проверяем что тесты проходят
echo "🧪 Running tests..."
pytest tests/ -v --tb=short

# Сборка
echo "🏗️ Building..."
rm -rf dist/ build/ *.egg-info/
python -m build

# Проверка
echo "🔍 Checking..."
python -m twine check dist/*

# Подтверждение
read -p "Upload to PyPI? (y/N): " confirm
if [ "$confirm" != "y" ]; then
    echo "❌ Cancelled"
    exit 0
fi

# Публикация
echo "🚀 Uploading to PyPI..."
python -m twine upload dist/*

echo "✅ Published!"
echo ""
echo "Install with:"
echo "  pip install ai-toolkit==$VERSION"


# Publish to PyPI

set -euo pipefail

# Проверяем что мы не забыли обновить версию
VERSION=$(grep 'version = ' pyproject.toml | head -1 | cut -d'"' -f2)
echo "📦 Publishing AI Toolkit v$VERSION"

# Проверяем что тесты проходят
echo "🧪 Running tests..."
pytest tests/ -v --tb=short

# Сборка
echo "🏗️ Building..."
rm -rf dist/ build/ *.egg-info/
python -m build

# Проверка
echo "🔍 Checking..."
python -m twine check dist/*

# Подтверждение
read -p "Upload to PyPI? (y/N): " confirm
if [ "$confirm" != "y" ]; then
    echo "❌ Cancelled"
    exit 0
fi

# Публикация
echo "🚀 Uploading to PyPI..."
python -m twine upload dist/*

echo "✅ Published!"
echo ""
echo "Install with:"
echo "  pip install ai-toolkit==$VERSION"


# Publish to PyPI

set -euo pipefail

# Проверяем что мы не забыли обновить версию
VERSION=$(grep 'version = ' pyproject.toml | head -1 | cut -d'"' -f2)
echo "📦 Publishing AI Toolkit v$VERSION"

# Проверяем что тесты проходят
echo "🧪 Running tests..."
pytest tests/ -v --tb=short

# Сборка
echo "🏗️ Building..."
rm -rf dist/ build/ *.egg-info/
python -m build

# Проверка
echo "🔍 Checking..."
python -m twine check dist/*

# Подтверждение
read -p "Upload to PyPI? (y/N): " confirm
if [ "$confirm" != "y" ]; then
    echo "❌ Cancelled"
    exit 0
fi

# Публикация
echo "🚀 Uploading to PyPI..."
python -m twine upload dist/*

echo "✅ Published!"
echo ""
echo "Install with:"
echo "  pip install ai-toolkit==$VERSION"

