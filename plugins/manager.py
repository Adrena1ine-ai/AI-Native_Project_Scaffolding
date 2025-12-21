"""
🔌 Plugin Manager — plugin management
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
    """Extension points (hooks)"""
    # Project creation
    PRE_CREATE = "pre_create"          # Before project creation
    POST_CREATE = "post_create"        # After project creation
    
    # File generation
    GENERATE_FILES = "generate_files"  # Generate additional files
    
    # Templates
    REGISTER_TEMPLATES = "register_templates"  # Register templates
    
    # Commands
    REGISTER_COMMANDS = "register_commands"    # Register commands
    
    # IDE
    REGISTER_IDE = "register_ide"      # Register IDE


class HookHandler(Protocol):
    """Protocol for hook handler"""
    def __call__(self, **kwargs: Any) -> Any:
        ...


@dataclass
class Plugin:
    """Plugin representation"""
    name: str
    version: str
    description: str = ""
    author: str = ""
    path: Path | None = None
    
    # Metadata
    enabled: bool = True
    dependencies: list[str] = field(default_factory=list)
    
    # Functionality
    templates: dict[str, dict] = field(default_factory=dict)
    commands: dict[str, Callable] = field(default_factory=dict)
    hooks: dict[PluginHook, list[HookHandler]] = field(default_factory=dict)
    
    # Module
    _module: Any = None
    
    def __post_init__(self):
        if not self.hooks:
            self.hooks = {hook: [] for hook in PluginHook}


# ══════════════════════════════════════════════════════════════
# Plugin Manager
# ══════════════════════════════════════════════════════════════

class PluginManager:
    """Plugin manager"""
    
    def __init__(self, plugins_dir: Path | None = None):
        """
        Args:
            plugins_dir: Directory with plugins
        """
        self.plugins_dir = plugins_dir or self._get_default_plugins_dir()
        self.plugins: dict[str, Plugin] = {}
        self._hooks: dict[PluginHook, list[tuple[str, HookHandler]]] = {
            hook: [] for hook in PluginHook
        }
    
    @staticmethod
    def _get_default_plugins_dir() -> Path:
        """Get default plugins directory"""
        # First check local folder
        local = Path(__file__).parent / "installed"
        if local.exists():
            return local
        
        # Then user directory
        user_dir = Path.home() / ".ai_toolkit" / "plugins"
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir
    
    def discover_plugins(self) -> list[str]:
        """
        Discover available plugins
        
        Returns:
            List of plugin names
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
        Load plugin
        
        Args:
            name: Plugin name
            
        Returns:
            Plugin object or None
        """
        if name in self.plugins:
            return self.plugins[name]
        
        # Plugin path
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
            # Load module
            spec = importlib.util.spec_from_file_location(
                f"ai_toolkit.plugins.{name}",
                plugin_path
            )
            if spec is None or spec.loader is None:
                return None
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            
            # Read metadata
            metadata = {}
            if metadata_path and metadata_path.exists():
                metadata = yaml.safe_load(metadata_path.read_text())
            
            # Create plugin object
            plugin = Plugin(
                name=metadata.get("name", name),
                version=metadata.get("version", "0.0.0"),
                description=metadata.get("description", ""),
                author=metadata.get("author", ""),
                path=plugin_path.parent if plugin_path.parent.name == name else None,
                dependencies=metadata.get("dependencies", []),
                _module=module,
            )
            
            # Call register() if exists
            if hasattr(module, "register"):
                module.register(plugin, self)
            
            self.plugins[name] = plugin
            return plugin
            
        except Exception as e:
            print(f"❌ Error loading plugin {name}: {e}")
            return None
    
    def load_all_plugins(self) -> int:
        """
        Load all plugins
        
        Returns:
            Number of loaded plugins
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
        Register hook handler
        
        Args:
            plugin_name: Plugin name
            hook: Hook type
            handler: Handler function
        """
        self._hooks[hook].append((plugin_name, handler))
        
        if plugin_name in self.plugins:
            self.plugins[plugin_name].hooks[hook].append(handler)
    
    def call_hook(self, hook: PluginHook, **kwargs: Any) -> list[Any]:
        """
        Call all hook handlers
        
        Args:
            hook: Hook type
            **kwargs: Arguments for handlers
            
        Returns:
            List of results
        """
        results = []
        
        for plugin_name, handler in self._hooks[hook]:
            try:
                result = handler(**kwargs)
                results.append(result)
            except Exception as e:
                print(f"⚠️ Error in {plugin_name}.{hook.value}: {e}")
        
        return results
    
    def get_plugin(self, name: str) -> Plugin | None:
        """Get plugin by name"""
        return self.plugins.get(name)
    
    def list_plugins(self) -> list[Plugin]:
        """Get list of all plugins"""
        return list(self.plugins.values())
    
    def get_all_templates(self) -> dict[str, dict]:
        """Get all templates from plugins"""
        templates = {}
        for plugin in self.plugins.values():
            templates.update(plugin.templates)
        return templates
    
    def get_all_commands(self) -> dict[str, Callable]:
        """Get all commands from plugins"""
        commands = {}
        for plugin in self.plugins.values():
            commands.update(plugin.commands)
        return commands


# ══════════════════════════════════════════════════════════════
# Helper Functions
# ══════════════════════════════════════════════════════════════

def create_plugin_skeleton(name: str, output_dir: Path) -> Path:
    """
    Create new plugin skeleton
    
    Args:
        name: Plugin name
        output_dir: Directory to create in
        
    Returns:
        Path to created plugin
    """
    plugin_dir = output_dir / name
    plugin_dir.mkdir(parents=True, exist_ok=True)
    
    # __init__.py
    init_content = f'''"""
{name} — plugin for AI Toolkit
"""

from plugins import Plugin, PluginManager, PluginHook


def register(plugin: Plugin, manager: PluginManager) -> None:
    """
    Register plugin
    
    Args:
        plugin: Plugin object
        manager: Plugin manager
    """
    # Register hook for project creation
    manager.register_hook(
        plugin.name,
        PluginHook.POST_CREATE,
        on_project_created,
    )
    
    # Add templates
    plugin.templates["custom"] = {{
        "name": "Custom Template",
        "description": "My custom template",
        "modules": ["custom"],
        "icon": "🔧",
    }}


def on_project_created(project_dir, project_name, **kwargs):
    """Called after project creation"""
    print(f"🔌 {name}: project {{project_name}} created!")
'''
    (plugin_dir / "__init__.py").write_text(init_content)
    
    # plugin.yaml
    yaml_content = f'''# {name} Plugin
name: "{name}"
version: "1.0.0"
description: "Plugin description"
author: "Your Name"

# Dependencies (other plugins)
dependencies: []

# Plugin settings
settings:
  enabled: true
'''
    (plugin_dir / "plugin.yaml").write_text(yaml_content)
    
    # README.md
    readme_content = f'''# {name}

Plugin for AI Toolkit.

## Installation

Copy folder `{name}` to `~/.ai_toolkit/plugins/`.

## Usage

Plugin loads automatically when AI Toolkit starts.

## Features

- Plugin feature description
'''
    (plugin_dir / "README.md").write_text(readme_content)
    
    return plugin_dir


# ══════════════════════════════════════════════════════════════
# Global instance
# ══════════════════════════════════════════════════════════════

# Global plugin manager
_manager: PluginManager | None = None


def get_plugin_manager() -> PluginManager:
    """Get global plugin manager"""
    global _manager
    if _manager is None:
        _manager = PluginManager()
    return _manager
