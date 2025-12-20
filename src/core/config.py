"""
Работа с конфигурацией
"""

from __future__ import annotations

import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Any

from .constants import IDE_CONFIGS, TEMPLATES, CLEANUP_LEVELS


@dataclass
class Config:
    """Главный конфиг Toolkit"""
    version: str = "3.0.0"
    
    # Пути
    venvs_path: str = "../_venvs"
    data_path: str = "../_data"
    artifacts_path: str = "../_artifacts"
    
    # Дефолты
    default_template: str = "bot"
    default_ide: str = "all"
    include_docker: bool = True
    include_ci: bool = True
    include_git: bool = True
    
    # Плагины
    plugins_dir: str = "~/.ai_toolkit/plugins"
    
    @classmethod
    def load(cls, path: Optional[Path] = None) -> Config:
        """Загрузить конфиг из файла"""
        if path is None:
            path = Path(__file__).parent.parent.parent / "toolkit.yaml"
        
        if not path.exists():
            return cls()
        
        try:
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            
            return cls(
                version=data.get("version", "3.0.0"),
                venvs_path=data.get("paths", {}).get("venvs", "../_venvs"),
                data_path=data.get("paths", {}).get("data", "../_data"),
                artifacts_path=data.get("paths", {}).get("artifacts", "../_artifacts"),
                default_template=data.get("defaults", {}).get("template", "bot"),
                default_ide=data.get("defaults", {}).get("ide", "all"),
                include_docker=data.get("defaults", {}).get("docker", True),
                include_ci=data.get("defaults", {}).get("ci", True),
                include_git=data.get("defaults", {}).get("git", True),
                plugins_dir=data.get("plugins_dir", "~/.ai_toolkit/plugins"),
            )
        except Exception:
            return cls()
    
    def save(self, path: Optional[Path] = None) -> None:
        """Сохранить конфиг"""
        if path is None:
            path = Path(__file__).parent.parent.parent / "toolkit.yaml"
        
        data = {
            "version": self.version,
            "paths": {
                "venvs": self.venvs_path,
                "data": self.data_path,
                "artifacts": self.artifacts_path,
            },
            "defaults": {
                "template": self.default_template,
                "ide": self.default_ide,
                "docker": self.include_docker,
                "ci": self.include_ci,
                "git": self.include_git,
            },
            "plugins_dir": self.plugins_dir,
        }
        
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    
    def get_template(self, name: str) -> Optional[dict]:
        """Получить шаблон по имени"""
        return TEMPLATES.get(name)
    
    def get_ide_config(self, name: str) -> Optional[dict]:
        """Получить конфиг IDE"""
        return IDE_CONFIGS.get(name)
    
    def get_cleanup_level(self, name: str) -> Optional[dict]:
        """Получить уровень очистки"""
        return CLEANUP_LEVELS.get(name)


# === Глобальное состояние ===

_config: Optional[Config] = None
_current_ide: str = "all"
_current_ai_targets: list[str] = ["cursor", "copilot", "claude", "windsurf"]
_current_language: str = "en"  # Default language


def get_config() -> Config:
    """Получить глобальный конфиг"""
    global _config
    if _config is None:
        _config = Config.load()
    return _config


def set_default_ide(ide: str, ai_targets: list[str]) -> None:
    """Установить IDE для текущей сессии"""
    global _current_ide, _current_ai_targets
    _current_ide = ide
    _current_ai_targets = ai_targets


def get_default_ide() -> str:
    """Получить текущую IDE"""
    return _current_ide


def get_default_ai_targets() -> list[str]:
    """Получить AI targets для текущей IDE"""
    return _current_ai_targets.copy()


# === Language settings ===

def get_language() -> str:
    """Get current language code ('en' or 'ru')."""
    global _current_language
    
    # Try to load from user config
    user_config_path = Path.home() / ".ai_toolkit" / "config.yaml"
    if user_config_path.exists():
        try:
            with open(user_config_path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                _current_language = data.get("language", "en")
        except Exception:
            pass
    
    return _current_language


def set_language(lang: str) -> None:
    """
    Set current language and save to user config.
    
    Args:
        lang: Language code ('en' or 'ru')
    """
    global _current_language
    _current_language = lang
    
    # Save to user config
    user_config_dir = Path.home() / ".ai_toolkit"
    user_config_dir.mkdir(parents=True, exist_ok=True)
    
    user_config_path = user_config_dir / "config.yaml"
    
    # Load existing config or create new
    data: dict[str, Any] = {}
    if user_config_path.exists():
        try:
            with open(user_config_path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except Exception:
            pass
    
    # Update language
    data["language"] = lang
    
    # Save
    with open(user_config_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def is_first_run() -> bool:
    """Check if this is the first run (no user config exists)."""
    user_config_path = Path.home() / ".ai_toolkit" / "config.yaml"
    return not user_config_path.exists()
