"""
Генератор основных файлов проекта (config, requirements, README)
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime

from ..core.file_utils import create_file
from ..core.constants import COLORS, TEMPLATES, VERSION


def generate_requirements(project_dir: Path, project_name: str, template: str) -> None:
    """Генерация requirements.txt"""
    
    # Базовые зависимости
    deps = [
        "# Core",
        "python-dotenv>=1.0",
        "pydantic>=2.6",
        "pydantic-settings>=2.2",
        "",
    ]
    
    tmpl = TEMPLATES.get(template, {})
    modules = tmpl.get("modules", [])
    
    # Telegram Bot
    if "bot" in modules or "handlers" in modules:
        deps.extend([
            "# Telegram Bot",
            "aiogram>=3.4",
            "aiohttp>=3.9",
            "",
        ])
    
    # Database
    if "database" in modules:
        deps.extend([
            "# Database",
            "aiosqlite>=0.20",
            "# sqlalchemy>=2.0  # если нужен ORM",
            "",
        ])
    
    # FastAPI
    if "api" in modules and template == "fastapi":
        deps.extend([
            "# FastAPI",
            "fastapi>=0.110",
            "uvicorn[standard]>=0.29",
            "",
        ])
    
    # Parser
    if "parser" in modules:
        deps.extend([
            "# Parser/Scraper",
            "httpx>=0.27",
            "beautifulsoup4>=4.12",
            "lxml>=5.1",
            "# playwright>=1.42  # если нужен браузер",
            "",
        ])
    
    content = f"# Requirements — {project_name}\n\n" + "\n".join(deps)
    create_file(project_dir / "requirements.txt", content)


def generate_requirements_dev(project_dir: Path) -> None:
    """Генерация requirements-dev.txt"""
    content = """# Development dependencies

# Testing
pytest>=8.0
pytest-asyncio>=0.23
pytest-cov>=4.1

# Linting & Formatting
ruff>=0.3

# Type checking
mypy>=1.9

# Pre-commit
pre-commit>=3.6

# Debug
ipython>=8.22
"""
    create_file(project_dir / "requirements-dev.txt", content)


def generate_env_example(project_dir: Path, project_name: str, template: str) -> None:
    """Генерация .env.example"""
    
    lines = [
        f"# Environment — {project_name}",
        "# Copy to .env and fill in values",
        "",
        "# App",
        "DEBUG=false",
        "",
    ]
    
    tmpl = TEMPLATES.get(template, {})
    modules = tmpl.get("modules", [])
    
    if "bot" in modules:
        lines.extend([
            "# Telegram Bot",
            "BOT_TOKEN=your_bot_token_here",
            "",
        ])
    
    if "database" in modules:
        lines.extend([
            "# Database",
            "DATABASE_PATH=database/app.sqlite3",
            "# DATABASE_URL=postgresql://user:pass@localhost/db",
            "",
        ])
    
    if "api" in modules:
        lines.extend([
            "# API",
            "API_HOST=0.0.0.0",
            "API_PORT=8000",
            "# SECRET_KEY=your-secret-key",
            "",
        ])
    
    content = "\n".join(lines)
    create_file(project_dir / ".env.example", content)


def generate_config_py(project_dir: Path, project_name: str, template: str) -> None:
    """Генерация config.py"""
    
    tmpl = TEMPLATES.get(template, {})
    modules = tmpl.get("modules", [])
    
    # Поля конфига
    fields = ['    debug: bool = False']
    
    if "bot" in modules:
        fields.append('    bot_token: str = ""')
    
    if "database" in modules:
        fields.append('    database_path: Path = Path("database/app.sqlite3")')
    
    if "api" in modules:
        fields.extend([
            '    api_host: str = "0.0.0.0"',
            '    api_port: int = 8000',
        ])
    
    fields_str = "\n".join(fields)
    
    content = f'''"""
Configuration — {project_name}
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
{fields_str}


# Global settings instance
settings = Settings()
'''
    create_file(project_dir / "config.py", content)


def generate_readme(project_dir: Path, project_name: str, template: str) -> None:
    """Генерация README.md"""
    
    tmpl = TEMPLATES.get(template, {})
    description = tmpl.get("description", "Project")
    
    # Quick start в зависимости от шаблона
    run_cmd = {
        "bot": "python bot/main.py",
        "webapp": "python -m http.server 8000 --directory webapp",
        "fastapi": "uvicorn api.main:app --reload",
        "parser": "python parser/main.py",
        "full": "python bot/main.py",
    }.get(template, "python main.py")
    
    content = f"""# 🚀 {project_name}

{description}

## 📋 Requirements

- Python 3.10+
- See `requirements.txt`

## 🚀 Quick Start

```bash
# 1. Bootstrap (создаёт venv ВНЕ проекта)
./scripts/bootstrap.sh

# 2. Активация
source ../_venvs/{project_name}-venv/bin/activate

# 3. Настройка
cp .env.example .env
# Отредактируй .env

# 4. Запуск
{run_cmd}
```

## 🐳 Docker

```bash
# Build & Run
docker-compose up -d

# Логи
docker-compose logs -f

# Остановка
docker-compose down
```

## 📁 Structure

```
{project_name}/
├── _AI_INCLUDE/        # Правила для AI
├── bot/                # Telegram bot
├── webapp/             # Mini App
├── api/                # API server
├── database/           # Database
├── scripts/            # Helper scripts
├── logs/               # Logs (gitignored)
├── data/               # Data (gitignored)
├── .github/            # GitHub Actions
├── Dockerfile
└── docker-compose.yml
```

## 🏥 Health Check

```bash
./scripts/health_check.sh
```

## 🎮 Context Switcher

Если AI тупит на большом проекте:

```bash
python scripts/context.py bot     # Фокус на боте
python scripts/context.py webapp  # Фокус на webapp
python scripts/context.py all     # Всё видно
```

## 🧪 Testing

```bash
pytest
pytest --cov=.
```

## 📝 License

MIT

---

Generated by [AI Toolkit v{VERSION}](https://github.com/mickhael/ai-toolkit)
"""
    create_file(project_dir / "README.md", content)


def generate_toolkit_version(project_dir: Path) -> None:
    """Генерация .toolkit-version"""
    create_file(project_dir / ".toolkit-version", VERSION)


def generate_pyproject_toml(project_dir: Path, project_name: str) -> None:
    """Генерация pyproject.toml"""
    content = f"""[project]
name = "{project_name}"
version = "0.1.0"
description = ""
requires-python = ">=3.10"

[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["{project_name.replace('-', '_')}"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.mypy]
python_version = "3.10"
strict = false
warn_return_any = true
warn_unused_ignores = true
"""
    create_file(project_dir / "pyproject.toml", content)


def generate_project_files(
    project_dir: Path,
    project_name: str,
    template: str
) -> None:
    """
    Создать основные файлы проекта
    
    Args:
        project_dir: Путь к проекту
        project_name: Название проекта
        template: Шаблон проекта
    """
    print(f"\n{COLORS.colorize('📦 Project files...', COLORS.CYAN)}")
    
    generate_requirements(project_dir, project_name, template)
    generate_requirements_dev(project_dir)
    generate_env_example(project_dir, project_name, template)
    generate_config_py(project_dir, project_name, template)
    generate_readme(project_dir, project_name, template)
    generate_toolkit_version(project_dir)
    generate_pyproject_toml(project_dir, project_name)
    
    # Создаём пустые директории
    for d in ["logs", "data", "tests"]:
        (project_dir / d).mkdir(exist_ok=True)
        create_file(project_dir / d / ".gitkeep", "", quiet=True)
    
    print(f"  {COLORS.success('logs/, data/, tests/')}")
