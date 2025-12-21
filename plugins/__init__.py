"""
🔌 AI Toolkit Plugin System

Plugin system for extending AI Toolkit functionality.

Plugins allow you to:
- Add new project templates
- Add new commands
- Extend generators
- Add support for new IDEs

Plugin structure:
    my_plugin/
    ├── __init__.py          # Entry point with register()
    ├── plugin.yaml          # Plugin metadata
    ├── templates/           # Templates (optional)
    └── generators/          # Generators (optional)
"""

from .manager import PluginManager, Plugin, PluginHook

__all__ = ["PluginManager", "Plugin", "PluginHook"]
