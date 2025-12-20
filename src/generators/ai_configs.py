"""
Генератор AI конфигов (.cursorrules, copilot-instructions.md, CLAUDE.md)
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime

from ..core.file_utils import create_file
from ..core.constants import COLORS


def get_common_rules(project_name: str, date: str) -> str:
    """Общие правила для всех AI"""
    return f"""# Project: {project_name}
# Generated: {date}

## 🧠 ПЕРВОЕ ДЕЙСТВИЕ

Прочитай `_AI_INCLUDE/` — там все правила проекта.

## 🚫 ЗАПРЕТЫ

- НЕ создавай venv/, .venv/ внутри проекта → используй ../_venvs/
- НЕ читай целиком большие файлы (logs, csv, sqlite)
- НЕ дублируй существующие файлы

## ✅ ПРАВИЛЬНЫЕ ДЕЙСТВИЯ

```bash
# Активация venv
source ../_venvs/{project_name}-venv/bin/activate

# Чтение данных
head -10 data/file.csv
tail -50 logs/bot.log
sqlite3 database/app.sqlite3 ".schema"
```

## 🎮 Context Switcher

```bash
python scripts/context.py bot   # Фокус на боте
python scripts/context.py all   # Всё видно
```
"""


def generate_cursor_rules(project_dir: Path, project_name: str, date: str) -> None:
    """Генерация .cursorrules"""
    content = get_common_rules(project_name, date)
    create_file(project_dir / ".cursorrules", content)


def generate_cursor_ignore(project_dir: Path, project_name: str, date: str) -> None:
    """Генерация .cursorignore"""
    content = f"""# Cursor Ignore — {project_name}
# Generated: {date}

# Environments
venv/
.venv/
**/.venv*/
**/site-packages/

# Python
**/__pycache__/
**/*.pyc
**/*.pyo
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Logs & Data
logs/
*.log
**/*.csv
**/*.jsonl
**/*.db
**/*.sqlite
**/*.sqlite3

# Frontend
node_modules/
dist/
build/
.next/

# Playwright
**/playwright/driver/

# IDE & Git
.git/
.idea/
*.swp
"""
    create_file(project_dir / ".cursorignore", content)


def generate_copilot_instructions(project_dir: Path, project_name: str, date: str) -> None:
    """Генерация .github/copilot-instructions.md"""
    content = f"""# Copilot Instructions — {project_name}

{get_common_rules(project_name, date)}

## Дополнительно для Copilot

- Используй type hints в Python коде
- Предпочитай async/await для I/O операций
- Следуй структуре проекта в _AI_INCLUDE/
- Используй pydantic для валидации данных
"""
    (project_dir / ".github").mkdir(exist_ok=True)
    create_file(project_dir / ".github" / "copilot-instructions.md", content)


def generate_claude_md(project_dir: Path, project_name: str, date: str) -> None:
    """Генерация CLAUDE.md"""
    content = f"""# Claude Instructions — {project_name}

{get_common_rules(project_name, date)}

## Дополнительно для Claude

- При работе с файлами сначала проверяй их существование
- Используй view tool для чтения _AI_INCLUDE/
- Предлагай изменения через str_replace
- Не читай большие файлы целиком
"""
    create_file(project_dir / "CLAUDE.md", content)


def generate_windsurf_rules(project_dir: Path, project_name: str, date: str) -> None:
    """Генерация .windsurfrules"""
    content = get_common_rules(project_name, date)
    create_file(project_dir / ".windsurfrules", content)


def generate_ai_include(project_dir: Path, project_name: str, date: str) -> None:
    """Генерация _AI_INCLUDE/"""
    ai_dir = project_dir / "_AI_INCLUDE"
    ai_dir.mkdir(exist_ok=True)
    
    # PROJECT_CONVENTIONS.md
    conventions = f"""# Project Conventions — {project_name}
# Этот файл читает AI. Люди тоже могут.

## Source code (read/edit freely)
bot/, handlers/, utils/, api/, webapp/, parser/, database/ — *.py files

## Never create venv inside repo
❌ Do NOT create: venv/, .venv/, */.venv*/
✅ Use external: ../_venvs/{project_name}-venv

Create via: ./scripts/bootstrap.sh

## Artifacts
- Logs: logs/ (gitignored)
- Data: data/ (gitignored)
- Heavy: ../_data/{project_name}/

## Before creating any file
1. Check _AI_INCLUDE/WHERE_IS_WHAT.md
2. Verify file doesn't exist
3. Use correct directory
"""
    create_file(ai_dir / "PROJECT_CONVENTIONS.md", conventions)
    
    # WHERE_IS_WHAT.md
    where_is_what = f"""# Where Is What — {project_name}

## Code Structure
```
bot/handlers/     — command handlers
bot/keyboards/    — keyboards
bot/utils/        — utilities
webapp/           — Mini App (HTML/JS/CSS)
scripts/          — helper scripts
database/         — DB operations
api/              — API server
```

## Data (DON'T read fully)
```
logs/             → tail -50 logs/bot.log
data/             → head -10 data/file.csv
database/*.db     → sqlite3 ... ".schema"
```

## Virtual Environment
Location: ../_venvs/{project_name}-venv/
Activate: source ../_venvs/{project_name}-venv/bin/activate
"""
    create_file(ai_dir / "WHERE_IS_WHAT.md", where_is_what)


def generate_ai_configs(
    project_dir: Path,
    project_name: str,
    ai_targets: list[str],
    date: str = None
) -> None:
    """
    Создать все AI конфиги
    
    Args:
        project_dir: Путь к проекту
        project_name: Название проекта
        ai_targets: Список AI (cursor, copilot, claude, windsurf)
        date: Дата (по умолчанию сегодня)
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n{COLORS.colorize('📄 AI configs...', COLORS.CYAN)}")
    
    # Cursor
    if "cursor" in ai_targets:
        generate_cursor_rules(project_dir, project_name, date)
        generate_cursor_ignore(project_dir, project_name, date)
    
    # Copilot
    if "copilot" in ai_targets:
        generate_copilot_instructions(project_dir, project_name, date)
    
    # Claude
    if "claude" in ai_targets:
        generate_claude_md(project_dir, project_name, date)
    
    # Windsurf
    if "windsurf" in ai_targets:
        generate_windsurf_rules(project_dir, project_name, date)
    
    # _AI_INCLUDE всегда
    print(f"\n{COLORS.colorize('📂 _AI_INCLUDE/...', COLORS.CYAN)}")
    generate_ai_include(project_dir, project_name, date)
