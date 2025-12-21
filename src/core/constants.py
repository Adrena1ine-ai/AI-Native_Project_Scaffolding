"""
Project constants
"""

VERSION = "3.0.0"


class COLORS:
    """ANSI colors for terminal"""
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
        """Colorize text"""
        return f"{color}{text}{cls.END}"
    
    @classmethod
    def success(cls, text: str) -> str:
        return cls.colorize(f"[OK] {text}", cls.GREEN)
    
    @classmethod
    def error(cls, text: str) -> str:
        return cls.colorize(f"[ERROR] {text}", cls.RED)
    
    @classmethod
    def warning(cls, text: str) -> str:
        return cls.colorize(f"[WARN] {text}", cls.YELLOW)
    
    @classmethod
    def info(cls, text: str) -> str:
        return cls.colorize(f"[INFO] {text}", cls.CYAN)


# IDE configurations
IDE_CONFIGS = {
    "cursor": {
        "name": "Cursor",
        "icon": "C",
        "files": [".cursorrules", ".cursorignore"],
        "ai_targets": ["cursor"],
    },
    "vscode_copilot": {
        "name": "VS Code + Copilot",
        "icon": "GH",
        "files": [".github/copilot-instructions.md"],
        "ai_targets": ["copilot"],
    },
    "vscode_claude": {
        "name": "VS Code + Claude",
        "icon": "CL",
        "files": ["CLAUDE.md"],
        "ai_targets": ["claude"],
    },
    "windsurf": {
        "name": "Windsurf",
        "icon": "WS",
        "files": [".windsurfrules"],
        "ai_targets": ["windsurf"],
    },
    "all": {
        "name": "Universal",
        "icon": "ALL",
        "files": ["all"],
        "ai_targets": ["cursor", "copilot", "claude", "windsurf"],
    },
}

# Project templates
TEMPLATES = {
    "bot": {
        "name": "Telegram Bot",
        "description": "Telegram bot using aiogram 3.x",
        "modules": ["bot", "handlers", "keyboards", "database"],
        "icon": "BOT",
    },
    "webapp": {
        "name": "Mini App",
        "description": "Telegram Mini App (HTML/JS/CSS)",
        "modules": ["webapp", "api"],
        "icon": "WEB",
    },
    "fastapi": {
        "name": "FastAPI",
        "description": "REST API using FastAPI",
        "modules": ["api", "database", "models"],
        "icon": "API",
    },
    "parser": {
        "name": "Web Parser",
        "description": "Web scraper/parser",
        "modules": ["parser", "database"],
        "icon": "PAR",
    },
    "full": {
        "name": "Full Stack",
        "description": "Bot + WebApp + API + Parser",
        "modules": ["bot", "webapp", "api", "parser", "database"],
        "icon": "FULL",
    },
    "monorepo": {
        "name": "Monorepo",
        "description": "Multiple projects in one repository",
        "modules": ["apps", "packages", "shared"],
        "icon": "MONO",
    },
}

# Cleanup levels
CLEANUP_LEVELS = {
    "safe": {
        "name": "Safe",
        "description": "Analysis and recommendations only",
        "actions": ["analyze", "report"],
    },
    "medium": {
        "name": "Medium",
        "description": "Move venv, create configs",
        "actions": ["analyze", "backup", "move_venv", "create_configs"],
    },
    "full": {
        "name": "Full",
        "description": "Complete restructuring",
        "actions": ["analyze", "backup", "move_venv", "move_data", "create_configs", "restructure"],
    },
}
