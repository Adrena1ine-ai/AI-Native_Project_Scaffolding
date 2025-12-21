# 🚀 Universal Project Generator

# One script — complete structure in a minute!

#!/usr/bin/env python3
"""
🚀 Project Generator: Telegram Bot + Mini App + Scripts
Creates complete structure with proper configuration for Cursor

Usage:
    python create_project.py my_awesome_bot
    python create_project.py my_bot --path /home/user/projects
"""

import argparse
import os
import stat
from pathlib import Path
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
# FILE TEMPLATES
# ═══════════════════════════════════════════════════════════════

CURSORIGNORE = '''# ═══════════════════════════════════════
# CURSOR IGNORE — DO NOT INDEX
# Generated: {date}
# ═══════════════════════════════════════

# === VIRTUAL ENVIRONMENTS ===
venv/
.venv/
env/
.env/
**/venv/
**/.venv/
**/site-packages/
**/lib/python*/
**/Lib/site-packages/
**/Scripts/
**/bin/python*

# === PLAYWRIGHT ===
**/playwright/driver/
**/playwright/.local-browsers/
**/.cache/ms-playwright/

# === PYTHON CACHES ===
__pycache__/
**/__pycache__/
*.py[cod]
*$py.class
*.pyo
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# === LOGS ===
logs/
*.log
*.log.*

# === DATA ===
data/
artifacts/
*.csv
*.sqlite3
*.sqlite
*.db

# === BINARIES ===
*.exe
*.so
*.dll
*.dylib

# === ASSETS ===
assets/
*.png
*.jpg
*.jpeg
*.gif
*.ico
*.webp
*.woff
*.woff2
*.ttf
*.eot

# === ARCHIVES ===
*.zip
*.tar
*.tar.gz
*.rar
*.7z

# === GIT ===
.git/

# === NODE ===
node_modules/
package-lock.json
yarn.lock

# === SECRETS ===
.env
.env.*
!.env.example
*.pem
*.key
*.secret

# === IDE ===
.idea/
.vscode/settings.json
*.swp
*.swo
*~
'''

CURSORRULES = '''# ═══════════════════════════════════════════════════════════
# RULES FOR AI — {project_name}
# Generated: {date}
# ═══════════════════════════════════════════════════════════

## 🧠 FIRST ACTION ON ANY REQUEST

1. Read `_AI_INCLUDE/` — all paths and rules are there
2. Check existing files before creating
3. Follow project structure

---

## 🚫 ABSOLUTE PROHIBITIONS

### Never create inside project:
- `venv/`, `.venv/`, `env/` — environments stored in `../_venvs/`
- Duplicates of existing files
- New requirements.txt in subfolders

### Never read entirely:
- `logs/*.log` → use `tail -50`
- `data/*.csv` → use `head -10`
- `*.sqlite3` → use SQL queries
- Any files > 100KB without explicit need

---

## ✅ CORRECT ACTIONS

### New Python package:
```bash
source ../_venvs/{project_name}-venv/bin/activate
pip install <package>
pip freeze > requirements.txt
```

### Data from CSV:
```bash
head -10 data/file.csv
grep -i "search" data/file.csv | head -5
wc -l data/file.csv
```

### DB structure:
```bash
sqlite3 database/app.sqlite3 ".schema"
sqlite3 database/app.sqlite3 "SELECT * FROM table LIMIT 5"
```

### Logs:
```bash
tail -50 logs/bot.log
grep -i "error" logs/bot.log | tail -20
```

---

## 📍 PROJECT STRUCTURE

### Code (read/edit freely):
```
bot/                 — Telegram bot
├── handlers/        — command handlers
├── keyboards/       — keyboards
├── utils/           — utilities
├── middlewares/     — middleware
└── main.py          — entry point

webapp/              — Mini App (HTML/JS/CSS)
scripts/             — Python scripts
database/db.py       — DB operations
api/                 — web server
config.py            — configuration
```

### Read carefully (only with good reason):
```
logs/               — logs (use tail/grep)
data/               — data files
database/*.sqlite3  — database
```

### Don't touch:
```
../_venvs/          — virtual environments
.git/               — git
```

---

## 🎯 AI BEHAVIOR

1. **Always read _AI_INCLUDE/ first**
2. Keep existing code and style
3. Use project conventions
4. Ask if unclear
'''

BOOTSTRAP_SH = '''#!/bin/bash
# ═══════════════════════════════════════════════════════════
# BOOTSTRAP — Creates venv OUTSIDE project
# ═══════════════════════════════════════════════════════════

set -e

PROJECT_NAME="{project_name}"
VENV_DIR="../_venvs/${{PROJECT_NAME}}-venv"

echo "🚀 Setting up $PROJECT_NAME..."

# Create _venvs directory
mkdir -p "$(dirname "$VENV_DIR")"

# Create venv if doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating venv in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# Activate and install
echo "📥 Installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Done!"
echo ""
echo "To activate:"
echo "  source $VENV_DIR/bin/activate"
'''

CONTEXT_SWITCHER = '''#!/usr/bin/env python3
"""
🎮 Context Switcher — Hide parts of project from AI
Usage:
    python context.py bot      # Focus on bot
    python context.py webapp   # Focus on webapp
    python context.py all      # Show all
    python context.py status   # Current status
"""

import sys
from pathlib import Path

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
    "bot": ["bot/", "handlers/"],
    "webapp": ["webapp/", "frontend/"],
    "parser": ["parser/"],
    "api": ["api/"],
    "database": ["database/"],
}

def update_cursorignore(mode: str):
    """Update .cursorignore for selected mode"""
    lines = [BASE_IGNORE.strip()]
    lines.append(f"\\n# === MODE: {mode.upper()} ===\\n")
    
    if mode == "all":
        lines.append("# All modules visible")
    elif mode in MODULES:
        for mod, paths in MODULES.items():
            if mod != mode:
                lines.append(f"# Hidden: {mod}")
                for p in paths:
                    lines.append(p)
    
    Path(".cursorignore").write_text("\\n".join(lines))
    print(f"✅ Mode set to: {mode.upper()}")

def show_status():
    """Show current mode"""
    ignore = Path(".cursorignore")
    if not ignore.exists():
        print("ℹ️ No .cursorignore found")
        return
    
    content = ignore.read_text()
    if "MODE:" in content:
        for line in content.split("\\n"):
            if "MODE:" in line:
                print(f"📍 Current: {line}")
                return
    print("📍 Current: default")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "status":
        show_status()
    elif cmd in MODULES or cmd == "all":
        update_cursorignore(cmd)
    else:
        print(f"❌ Unknown mode: {cmd}")
        print(f"Available: {', '.join(MODULES.keys())}, all")
'''


# ═══════════════════════════════════════════════════════════════
# PROJECT STRUCTURE
# ═══════════════════════════════════════════════════════════════

def create_file(path: Path, content: str = "", executable: bool = False) -> None:
    """Create file with content"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding='utf-8')
    
    if executable:
        os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
    
    print(f"  📄 {path}")


def create_project(name: str, base_path: Path) -> None:
    """Create project structure"""
    project_dir = base_path / name
    
    if project_dir.exists():
        print(f"❌ Directory {project_dir} already exists!")
        return
    
    date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"🚀 Creating project: {name}")
    print(f"📂 Path: {project_dir}")
    print()
    
    # Create directories
    for dir_name in [
        "bot/handlers",
        "bot/keyboards",
        "bot/utils",
        "bot/middlewares",
        "webapp",
        "database",
        "api",
        "scripts",
        "logs",
        "data",
        "_AI_INCLUDE",
    ]:
        (project_dir / dir_name).mkdir(parents=True, exist_ok=True)
    
    # Create files
    create_file(
        project_dir / ".cursorignore",
        CURSORIGNORE.format(date=date)
    )
    
    create_file(
        project_dir / ".cursorrules",
        CURSORRULES.format(project_name=name, date=date)
    )
    
    create_file(
        project_dir / "scripts/bootstrap.sh",
        BOOTSTRAP_SH.format(project_name=name),
        executable=True
    )
    
    create_file(
        project_dir / "scripts/context.py",
        CONTEXT_SWITCHER,
        executable=True
    )
    
    # Bot main.py
    create_file(
        project_dir / "bot/main.py",
        f'''"""
{name} — Telegram Bot
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
'''
    )
    
    # Config
    create_file(
        project_dir / "config.py",
        '''"""Configuration"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
'''
    )
    
    # Requirements
    create_file(
        project_dir / "requirements.txt",
        '''aiogram>=3.0
python-dotenv
pydantic-settings
'''
    )
    
    # .env.example
    create_file(
        project_dir / ".env.example",
        '''BOT_TOKEN=your_token_here
'''
    )
    
    # README
    create_file(
        project_dir / "README.md",
        f'''# {name}

## Quick Start

```bash
# 1. Create venv (OUTSIDE project!)
./scripts/bootstrap.sh

# 2. Activate
source ../_venvs/{name}-venv/bin/activate

# 3. Configure
cp .env.example .env
# Edit .env with your token

# 4. Run
python bot/main.py
```

## Structure

```
{name}/
├── bot/                 # Telegram bot
├── webapp/              # Mini App
├── database/            # DB operations
├── scripts/             # Utility scripts
├── _AI_INCLUDE/         # AI rules
└── config.py            # Configuration
```

## For AI

Read `_AI_INCLUDE/` first!
'''
    )
    
    # _AI_INCLUDE
    create_file(
        project_dir / "_AI_INCLUDE/PROJECT_CONVENTIONS.md",
        f'''# Project Conventions — {name}

## Key Rules

1. **venv** — always in `../_venvs/{name}-venv/`
2. **Structure** — follow existing patterns
3. **Logging** — use `logging` module
4. **Config** — use `config.py` and `.env`

## Code Style

- Python 3.10+
- Type hints
- Docstrings
- max 100 chars per line
'''
    )
    
    create_file(
        project_dir / "_AI_INCLUDE/WHERE_IS_WHAT.md",
        f'''# Where Is What — {name}

## Main Files

| What | Where |
|------|-------|
| Bot entry | `bot/main.py` |
| Config | `config.py` |
| Handlers | `bot/handlers/` |
| Database | `database/` |
| Scripts | `scripts/` |

## Key Commands

```bash
# Activate venv
source ../_venvs/{name}-venv/bin/activate

# Run bot
python bot/main.py

# Context switch
python scripts/context.py bot
```
'''
    )
    
    print()
    print("=" * 50)
    print(f"✅ Project {name} created!")
    print("=" * 50)
    print()
    print("Next steps:")
    print(f"  1. cd {project_dir}")
    print(f"  2. ./scripts/bootstrap.sh")
    print(f"  3. source ../_venvs/{name}-venv/bin/activate")
    print(f"  4. cp .env.example .env")
    print(f"  5. python bot/main.py")


def main():
    parser = argparse.ArgumentParser(
        description="Create AI-native project structure"
    )
    parser.add_argument("name", help="Project name")
    parser.add_argument(
        "--path", "-p",
        default=".",
        help="Base path (default: current directory)"
    )
    
    args = parser.parse_args()
    
    base_path = Path(args.path).resolve()
    create_project(args.name, base_path)


# For import from START.py
def run(project_name: str, base_path: Path = None):
    """Run builder from START.py"""
    if base_path is None:
        base_path = Path.cwd()
    create_project(project_name, base_path)


if __name__ == "__main__":
    main()
