"""
Команда create — создание нового проекта
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime

from ..core.constants import COLORS, TEMPLATES, VERSION
from ..core.config import get_config, get_default_ide, get_default_ai_targets
from ..core.file_utils import create_file

from ..generators import (
    generate_ai_configs,
    generate_scripts,
    generate_project_files,
    generate_docker_files,
    generate_ci_files,
    init_git_repo,
)


def select_template() -> str:
    """Интерактивный выбор шаблона"""
    print("\n📦 Выбери шаблон:\n")
    
    templates = list(TEMPLATES.items())
    for i, (name, tmpl) in enumerate(templates, 1):
        icon = tmpl.get("icon", "📁")
        desc = tmpl.get("description", "")
        print(f"  {i}. {icon} {tmpl['name']} — {desc}")
    
    while True:
        choice = input(f"\nВыбор (1-{len(templates)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(templates):
                return templates[idx][0]
        except ValueError:
            pass
        print("  Неверный выбор")


def generate_bot_module(project_dir: Path, project_name: str) -> None:
    """Генерация модуля бота"""
    
    for d in ["bot/handlers", "bot/keyboards", "bot/utils", "bot/middlewares"]:
        (project_dir / d).mkdir(parents=True, exist_ok=True)
    
    create_file(project_dir / "bot/__init__.py", '"""Bot package"""')
    
    main_content = f'''"""🤖 {project_name} — Telegram Bot"""

import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import settings
from bot.handlers import setup_handlers

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("🚀 Starting bot...")
    
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    setup_handlers(dp)
    
    try:
        logger.info("✅ Bot started!")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
'''
    create_file(project_dir / "bot/main.py", main_content)
    
    handlers_init = '''"""Handlers"""
from aiogram import Dispatcher
from .start import router as start_router

def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(start_router)
'''
    create_file(project_dir / "bot/handlers/__init__.py", handlers_init)
    
    start_content = '''"""Start handler"""
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"👋 Привет, <b>{message.from_user.first_name}</b>!")

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("📚 /start — Начать\\n/help — Помощь")
'''
    create_file(project_dir / "bot/handlers/start.py", start_content)
    
    for pkg in ["keyboards", "utils", "middlewares"]:
        create_file(project_dir / f"bot/{pkg}/__init__.py", f'"""{pkg}"""')


def generate_database_module(project_dir: Path) -> None:
    """Генерация модуля БД"""
    (project_dir / "database").mkdir(exist_ok=True)
    create_file(project_dir / "database/__init__.py", '"""Database"""')
    
    db_content = '''"""Database operations"""
import aiosqlite
from config import settings

async def init_db():
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(settings.database_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def get_user(telegram_id: int):
    async with aiosqlite.connect(settings.database_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)) as cur:
            return await cur.fetchone()
'''
    create_file(project_dir / "database/db.py", db_content)


def generate_api_module(project_dir: Path, project_name: str, template: str) -> None:
    """Генерация модуля API"""
    (project_dir / "api").mkdir(exist_ok=True)
    create_file(project_dir / "api/__init__.py", '"""API"""')
    
    if template == "fastapi":
        content = f'''"""⚡ {project_name} API"""
from fastapi import FastAPI
from config import settings

app = FastAPI(title="{project_name}", debug=settings.debug)

@app.get("/")
async def root():
    return {{"message": "Hello!"}}

@app.get("/health")
async def health():
    return {{"status": "ok"}}
'''
    else:
        content = '"""API — TODO"""'
    
    create_file(project_dir / "api/main.py", content)


def generate_webapp_module(project_dir: Path, project_name: str) -> None:
    """Генерация модуля WebApp"""
    (project_dir / "webapp").mkdir(exist_ok=True)
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
    <h1>🚀 {project_name}</h1>
    <script>
        const tg = window.Telegram.WebApp;
        tg.ready();
        tg.expand();
    </script>
</body>
</html>
'''
    create_file(project_dir / "webapp/index.html", html)


def generate_parser_module(project_dir: Path) -> None:
    """Генерация модуля парсера"""
    (project_dir / "parser").mkdir(exist_ok=True)
    create_file(project_dir / "parser/__init__.py", '"""Parser"""')
    
    content = '''"""Web Parser"""
import httpx
from bs4 import BeautifulSoup

async def fetch_page(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")
'''
    create_file(project_dir / "parser/scraper.py", content)


def generate_module_files(project_dir: Path, project_name: str, template: str) -> None:
    """Генерация файлов модулей"""
    tmpl = TEMPLATES.get(template, {})
    modules = tmpl.get("modules", [])
    
    print(f"\n{COLORS.colorize('📂 Modules...', COLORS.CYAN)}")
    
    if "bot" in modules or "handlers" in modules:
        generate_bot_module(project_dir, project_name)
    if "database" in modules:
        generate_database_module(project_dir)
    if "api" in modules:
        generate_api_module(project_dir, project_name, template)
    if "webapp" in modules:
        generate_webapp_module(project_dir, project_name)
    if "parser" in modules:
        generate_parser_module(project_dir)


def create_project(
    name: str,
    path: Path,
    template: str = "bot",
    ai_targets: list[str] = None,
    include_docker: bool = True,
    include_ci: bool = True,
    include_git: bool = True,
    include_manifesto: bool = True,
) -> bool:
    """
    Создать новый проект
    
    Args:
        name: Название проекта
        path: Базовый путь
        template: Шаблон
        ai_targets: Список AI
        include_docker: Добавить Docker
        include_ci: Добавить CI/CD
        include_git: Инициализировать Git
        include_manifesto: Включить manifesto
    """
    if ai_targets is None:
        ai_targets = get_default_ai_targets()
    
    project_dir = path / name
    date = datetime.now().strftime("%Y-%m-%d")
    
    if project_dir.exists():
        print(f"{COLORS.error(f'Папка уже существует: {project_dir}')}")
        return False
    
    tmpl = TEMPLATES.get(template, {})
    
    print(f"""
{COLORS.colorize('═' * 60, COLORS.CYAN)}
{COLORS.colorize(f'🆕 Creating project: {name}', COLORS.CYAN)}
{COLORS.colorize('═' * 60, COLORS.CYAN)}
📁 Path: {project_dir}
📦 Template: {tmpl.get('icon', '')} {tmpl.get('name', template)}
🤖 AI: {', '.join(ai_targets)}
🐳 Docker: {'Yes' if include_docker else 'No'}
🚀 CI/CD: {'Yes' if include_ci else 'No'}
🔗 Git: {'Yes' if include_git else 'No'}
""")
    
    # Создаём директорию
    project_dir.mkdir(parents=True)
    
    # AI конфиги
    generate_ai_configs(project_dir, name, ai_targets, date)
    
    # Scripts
    generate_scripts(project_dir, name)
    
    # Project files
    generate_project_files(project_dir, name, template)
    
    # Module files
    generate_module_files(project_dir, name, template)
    
    # Docker
    if include_docker:
        generate_docker_files(project_dir, name, template)
    
    # CI/CD
    if include_ci:
        generate_ci_files(project_dir, name)
    
    # Git
    if include_git:
        init_git_repo(project_dir, name)
    
    # Manifesto
    if include_manifesto:
        toolkit_dir = Path(__file__).parent.parent.parent
        manifesto_src = toolkit_dir / "docs" / "manifesto.md"
        if manifesto_src.exists():
            import shutil
            shutil.copy(manifesto_src, project_dir / "_AI_INCLUDE" / "FULL_MANIFESTO.md")
            print(f"  {COLORS.success('_AI_INCLUDE/FULL_MANIFESTO.md')}")
    
    print(f"""
{COLORS.colorize('═' * 60, COLORS.GREEN)}
{COLORS.colorize('✅ Project created!', COLORS.GREEN)}
{COLORS.colorize('═' * 60, COLORS.GREEN)}

Next steps:

  cd {project_dir}
  ./scripts/bootstrap.sh
  source ../_venvs/{name}-venv/bin/activate
  cp .env.example .env
  # Edit .env
""")
    
    return True


def cmd_create() -> None:
    """Интерактивная команда создания проекта"""
    from ..core.config import get_default_ide
    
    print(COLORS.colorize("\n🆕 СОЗДАНИЕ НОВОГО ПРОЕКТА\n", COLORS.GREEN))
    
    # Показываем IDE
    ide = get_default_ide()
    ide_names = {
        "cursor": "💜 Cursor",
        "vscode_copilot": "💙 VS Code + Copilot",
        "vscode_claude": "🟢 VS Code + Claude",
        "windsurf": "🌊 Windsurf",
        "all": "🔄 Универсальный",
    }
    print(f"  IDE: {ide_names.get(ide, ide)}\n")
    
    # Имя
    name = input("Название проекта: ").strip()
    if not name:
        print(COLORS.warning("Отменено"))
        return
    
    if not name.replace('_', '').replace('-', '').isalnum():
        print(COLORS.error("Название: только буквы, цифры, _ и -"))
        return
    
    # Путь
    path_str = input("Путь (Enter = текущая папка): ").strip()
    path = Path(path_str).resolve() if path_str else Path.cwd()
    
    # Шаблон
    template = select_template()
    
    # Опции
    print("\n📋 Опции:\n")
    include_docker = input("  Добавить Docker? (Y/n): ").strip().lower() != 'n'
    include_ci = input("  Добавить CI/CD? (Y/n): ").strip().lower() != 'n'
    include_git = input("  Инициализировать Git? (Y/n): ").strip().lower() != 'n'
    
    # Подтверждение
    confirm = input("\nСоздать проект? (Y/n): ").strip().lower()
    if confirm == 'n':
        print(COLORS.warning("Отменено"))
        return
    
    # Создание
    create_project(
        name=name,
        path=path,
        template=template,
        ai_targets=get_default_ai_targets(),
        include_docker=include_docker,
        include_ci=include_ci,
        include_git=include_git,
    )
