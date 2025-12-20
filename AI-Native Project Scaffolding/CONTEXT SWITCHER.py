#!/usr/bin/env python3
"""
🛠️ BUILDER (ГЕНЕРАТОР ПРОЕКТА)
Создает структуру, venv и скрипты.
"""
import sys
import os
import stat
from pathlib import Path

# === ТВОЯ КИЛЛЕР-ФИЧА: Context Switcher ===
CONTEXT_SCRIPT = '''#!/usr/bin/env python3
"""
🎮 CONTEXT SWITCHER — Авторская методика
Скрывает части проекта от Cursor, чтобы он не тупил.
"""
import sys

BASE_IGNORE = """
venv/
.venv/
.env
**/__pycache__/
.git/
logs/
data/
artifacts/
"""

MODULES = {
    "bot": ["bot/", "bot.py"],
    "webapp": ["webapp/", "frontend/"],
    "parser": ["parser/"],
    "api": ["api/"],
    "db": ["database/"]
}

def update(mode):
    lines = [BASE_IGNORE.strip(), f"\\n# === MODE: {mode.upper()} ===\\n"]
    if mode == "all":
        lines.append("# All modules visible")
    else:
        for m, paths in MODULES.items():
            if m != mode:
                lines.append(f"# Ignoring {m}")
                for p in paths: lines.append(p)
    
    with open(".cursorignore", "w", encoding="utf-8") as f:
        f.write("\\n".join(lines))
    print(f"✅ Режим: {mode.upper()}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python context.py [bot|webapp|parser|api|all]")
    else:
        update(sys.argv[1].lower())
'''

# === BOOTSTRAP SCRIPT ===
BOOTSTRAP = '''#!/bin/bash
set -e
PROJ=$(basename "$PWD")
VENV="../../_venvs/${PROJ}-venv"
echo "🚀 Setup $PROJ in $VENV"
mkdir -p "$VENV"
if [ ! -d "$VENV/bin" ]; then python3 -m venv "$VENV"; fi
echo "✅ Done. Run: source $VENV/bin/activate"
'''

def create_file(path: Path, content: str, exe=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding='utf-8')
    if exe: os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
    print(f"  📄 {path}")

def run(project_name):
    root = Path(project_name)
    if root.exists():
        print(f"❌ {project_name} уже есть!")
        return

    print(f"🏗️ Строю проект: {project_name}...")
    
    # Структура
    for d in ["bot", "webapp", "parser", "database", "api", "scripts", "_AI_INCLUDE"]:
        (root / d).mkdir(parents=True, exist_ok=True)

    # Создание файлов
    create_file(root / "scripts/context.py", CONTEXT_SCRIPT, exe=True)
    create_file(root / "scripts/bootstrap.sh", BOOTSTRAP, exe=True)
    create_file(root / ".cursorignore", "venv/\n.env\n")
    create_file(root / "README.md", f"# {project_name}\nCreated by AI Toolkit")
    
    # Сюда можно добавить создание main.py, handlers и т.д. из Файла 4
    
    print("✅ Готово.")

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "new_project")