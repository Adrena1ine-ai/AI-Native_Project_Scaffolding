"""
Константы проекта
"""

VERSION = "3.0.0"


class COLORS:
    """ANSI цвета для терминала"""
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    END = "\033[0m"
    
    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """Раскрасить текст"""
        return f"{color}{text}{cls.END}"
    
    @classmethod
    def success(cls, text: str) -> str:
        return cls.colorize(f"✅ {text}", cls.GREEN)
    
    @classmethod
    def error(cls, text: str) -> str:
        return cls.colorize(f"❌ {text}", cls.RED)
    
    @classmethod
    def warning(cls, text: str) -> str:
        return cls.colorize(f"⚠️  {text}", cls.YELLOW)
    
    @classmethod
    def info(cls, text: str) -> str:
        return cls.colorize(f"ℹ️  {text}", cls.CYAN)


# IDE конфигурации
IDE_CONFIGS = {
    "cursor": {
        "name": "Cursor",
        "icon": "💜",
        "files": [".cursorrules", ".cursorignore"],
        "ai_targets": ["cursor"],
    },
    "vscode_copilot": {
        "name": "VS Code + Copilot",
        "icon": "💙",
        "files": [".github/copilot-instructions.md"],
        "ai_targets": ["copilot"],
    },
    "vscode_claude": {
        "name": "VS Code + Claude",
        "icon": "🟢",
        "files": ["CLAUDE.md"],
        "ai_targets": ["claude"],
    },
    "windsurf": {
        "name": "Windsurf",
        "icon": "🌊",
        "files": [".windsurfrules"],
        "ai_targets": ["windsurf"],
    },
    "all": {
        "name": "Универсальный",
        "icon": "🔄",
        "files": ["all"],
        "ai_targets": ["cursor", "copilot", "claude", "windsurf"],
    },
}

# Шаблоны проектов
TEMPLATES = {
    "bot": {
        "name": "Telegram Bot",
        "description": "Telegram бот на aiogram 3.x",
        "modules": ["bot", "handlers", "keyboards", "database"],
        "icon": "🤖",
    },
    "webapp": {
        "name": "Mini App",
        "description": "Telegram Mini App (HTML/JS/CSS)",
        "modules": ["webapp", "api"],
        "icon": "🌐",
    },
    "fastapi": {
        "name": "FastAPI",
        "description": "REST API на FastAPI",
        "modules": ["api", "database", "models"],
        "icon": "⚡",
    },
    "parser": {
        "name": "Web Parser",
        "description": "Парсер/скрапер",
        "modules": ["parser", "database"],
        "icon": "🕷️",
    },
    "full": {
        "name": "Full Stack",
        "description": "Bot + WebApp + API + Parser",
        "modules": ["bot", "webapp", "api", "parser", "database"],
        "icon": "🚀",
    },
    "monorepo": {
        "name": "Monorepo",
        "description": "Несколько проектов в одном репозитории",
        "modules": ["apps", "packages", "shared"],
        "icon": "📦",
    },
}

# Уровни очистки
CLEANUP_LEVELS = {
    "safe": {
        "name": "Безопасный",
        "description": "Только анализ и рекомендации",
        "actions": ["analyze", "report"],
    },
    "medium": {
        "name": "Средний",
        "description": "Переместить venv, создать конфиги",
        "actions": ["analyze", "backup", "move_venv", "create_configs"],
    },
    "full": {
        "name": "Полный",
        "description": "Полная реструктуризация",
        "actions": ["analyze", "backup", "move_venv", "move_data", "create_configs", "restructure"],
    },
}
