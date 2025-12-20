"""
🔌 Plugin Manager — управление плагинами
"""

from __future__ import annotations

import sys
import importlib
import importlib.util
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol
from enum import Enum
import yaml


# ══════════════════════════════════════════════════════════════
# Types
# ══════════════════════════════════════════════════════════════

class PluginHook(Enum):
    """Точки расширения (hooks)"""
    # Создание проекта
    PRE_CREATE = "pre_create"          # Перед созданием проекта
    POST_CREATE = "post_create"        # После создания проекта
    
    # Генерация файлов
    GENERATE_FILES = "generate_files"  # Генерация дополнительных файлов
    
    # Шаблоны
    REGISTER_TEMPLATES = "register_templates"  # Регистрация шаблонов
    
    # Команды
    REGISTER_COMMANDS = "register_commands"    # Регистрация команд
    
    # IDE
    REGISTER_IDE = "register_ide"      # Регистрация IDE


class HookHandler(Protocol):
    """Протокол для обработчика hook"""
    def __call__(self, **kwargs: Any) -> Any:
        ...


@dataclass
class Plugin:
    """Представление плагина"""
    name: str
    version: str
    description: str = ""
    author: str = ""
    path: Path | None = None
    
    # Метаданные
    enabled: bool = True
    dependencies: list[str] = field(default_factory=list)
    
    # Функциональность
    templates: dict[str, dict] = field(default_factory=dict)
    commands: dict[str, Callable] = field(default_factory=dict)
    hooks: dict[PluginHook, list[HookHandler]] = field(default_factory=dict)
    
    # Модуль
    _module: Any = None
    
    def __post_init__(self):
        if not self.hooks:
            self.hooks = {hook: [] for hook in PluginHook}


# ══════════════════════════════════════════════════════════════
# Plugin Manager
# ══════════════════════════════════════════════════════════════

class PluginManager:
    """Менеджер плагинов"""
    
    def __init__(self, plugins_dir: Path | None = None):
        """
        Args:
            plugins_dir: Директория с плагинами
        """
        self.plugins_dir = plugins_dir or self._get_default_plugins_dir()
        self.plugins: dict[str, Plugin] = {}
        self._hooks: dict[PluginHook, list[tuple[str, HookHandler]]] = {
            hook: [] for hook in PluginHook
        }
    
    @staticmethod
    def _get_default_plugins_dir() -> Path:
        """Получить директорию плагинов по умолчанию"""
        # Сначала проверяем локальную папку
        local = Path(__file__).parent / "installed"
        if local.exists():
            return local
        
        # Затем пользовательскую
        user_dir = Path.home() / ".ai_toolkit" / "plugins"
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir
    
    def discover_plugins(self) -> list[str]:
        """
        Обнаружить доступные плагины
        
        Returns:
            Список имён плагинов
        """
        plugins = []
        
        if not self.plugins_dir.exists():
            return plugins
        
        for item in self.plugins_dir.iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                plugins.append(item.name)
            elif item.suffix == ".py" and item.stem != "__init__":
                plugins.append(item.stem)
        
        return plugins
    
    def load_plugin(self, name: str) -> Plugin | None:
        """
        Загрузить плагин
        
        Args:
            name: Имя плагина
            
        Returns:
            Объект плагина или None
        """
        if name in self.plugins:
            return self.plugins[name]
        
        # Путь к плагину
        plugin_dir = self.plugins_dir / name
        plugin_file = self.plugins_dir / f"{name}.py"
        
        if plugin_dir.is_dir():
            plugin_path = plugin_dir / "__init__.py"
            metadata_path = plugin_dir / "plugin.yaml"
        elif plugin_file.exists():
            plugin_path = plugin_file
            metadata_path = None
        else:
            return None
        
        try:
            # Загружаем модуль
            spec = importlib.util.spec_from_file_location(
                f"ai_toolkit.plugins.{name}",
                plugin_path
            )
            if spec is None or spec.loader is None:
                return None
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            
            # Читаем метаданные
            metadata = {}
            if metadata_path and metadata_path.exists():
                metadata = yaml.safe_load(metadata_path.read_text())
            
            # Создаём объект плагина
            plugin = Plugin(
                name=metadata.get("name", name),
                version=metadata.get("version", "0.0.0"),
                description=metadata.get("description", ""),
                author=metadata.get("author", ""),
                path=plugin_path.parent if plugin_path.parent.name == name else None,
                dependencies=metadata.get("dependencies", []),
                _module=module,
            )
            
            # Вызываем register() если есть
            if hasattr(module, "register"):
                module.register(plugin, self)
            
            self.plugins[name] = plugin
            return plugin
            
        except Exception as e:
            print(f"❌ Ошибка загрузки плагина {name}: {e}")
            return None
    
    def load_all_plugins(self) -> int:
        """
        Загрузить все плагины
        
        Returns:
            Количество загруженных плагинов
        """
        count = 0
        for name in self.discover_plugins():
            if self.load_plugin(name):
                count += 1
        return count
    
    def register_hook(
        self, 
        plugin_name: str, 
        hook: PluginHook, 
        handler: HookHandler
    ) -> None:
        """
        Зарегистрировать обработчик hook
        
        Args:
            plugin_name: Имя плагина
            hook: Тип hook
            handler: Функция-обработчик
        """
        self._hooks[hook].append((plugin_name, handler))
        
        if plugin_name in self.plugins:
            self.plugins[plugin_name].hooks[hook].append(handler)
    
    def call_hook(self, hook: PluginHook, **kwargs: Any) -> list[Any]:
        """
        Вызвать все обработчики hook
        
        Args:
            hook: Тип hook
            **kwargs: Аргументы для обработчиков
            
        Returns:
            Список результатов
        """
        results = []
        
        for plugin_name, handler in self._hooks[hook]:
            try:
                result = handler(**kwargs)
                results.append(result)
            except Exception as e:
                print(f"⚠️ Ошибка в {plugin_name}.{hook.value}: {e}")
        
        return results
    
    def get_plugin(self, name: str) -> Plugin | None:
        """Получить плагин по имени"""
        return self.plugins.get(name)
    
    def list_plugins(self) -> list[Plugin]:
        """Получить список всех плагинов"""
        return list(self.plugins.values())
    
    def get_all_templates(self) -> dict[str, dict]:
        """Получить все шаблоны из плагинов"""
        templates = {}
        for plugin in self.plugins.values():
            templates.update(plugin.templates)
        return templates
    
    def get_all_commands(self) -> dict[str, Callable]:
        """Получить все команды из плагинов"""
        commands = {}
        for plugin in self.plugins.values():
            commands.update(plugin.commands)
        return commands


# ══════════════════════════════════════════════════════════════
# Helper Functions
# ══════════════════════════════════════════════════════════════

def create_plugin_skeleton(name: str, output_dir: Path) -> Path:
    """
    Создать скелет нового плагина
    
    Args:
        name: Имя плагина
        output_dir: Директория для создания
        
    Returns:
        Путь к созданному плагину
    """
    plugin_dir = output_dir / name
    plugin_dir.mkdir(parents=True, exist_ok=True)
    
    # __init__.py
    init_content = f'''"""
{name} — плагин для AI Toolkit
"""

from plugins import Plugin, PluginManager, PluginHook


def register(plugin: Plugin, manager: PluginManager) -> None:
    """
    Регистрация плагина
    
    Args:
        plugin: Объект плагина
        manager: Менеджер плагинов
    """
    # Регистрируем hook для создания проекта
    manager.register_hook(
        plugin.name,
        PluginHook.POST_CREATE,
        on_project_created,
    )
    
    # Добавляем шаблоны
    plugin.templates["custom"] = {{
        "name": "Custom Template",
        "description": "Мой кастомный шаблон",
        "modules": ["custom"],
        "icon": "🔧",
    }}


def on_project_created(project_dir, project_name, **kwargs):
    """Вызывается после создания проекта"""
    print(f"🔌 {name}: проект {{project_name}} создан!")
'''
    (plugin_dir / "__init__.py").write_text(init_content)
    
    # plugin.yaml
    yaml_content = f'''# {name} Plugin
name: "{name}"
version: "1.0.0"
description: "Описание плагина"
author: "Your Name"

# Зависимости (другие плагины)
dependencies: []

# Настройки плагина
settings:
  enabled: true
'''
    (plugin_dir / "plugin.yaml").write_text(yaml_content)
    
    # README.md
    readme_content = f'''# {name}

Плагин для AI Toolkit.

## Установка

Скопируйте папку `{name}` в `~/.ai_toolkit/plugins/`.

## Использование

Плагин автоматически загружается при запуске AI Toolkit.

## Возможности

- Описание функций плагина
'''
    (plugin_dir / "README.md").write_text(readme_content)
    
    return plugin_dir


# ══════════════════════════════════════════════════════════════
# Global instance
# ══════════════════════════════════════════════════════════════

# Глобальный менеджер плагинов
_manager: PluginManager | None = None


def get_plugin_manager() -> PluginManager:
    """Получить глобальный менеджер плагинов"""
    global _manager
    if _manager is None:
        _manager = PluginManager()
    return _manager

