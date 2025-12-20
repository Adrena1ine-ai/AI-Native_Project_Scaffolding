"""
Команды CLI
"""

from .create import cmd_create, create_project
from .cleanup import cmd_cleanup, analyze_project, cleanup_project
from .migrate import cmd_migrate, migrate_project
from .health import cmd_health, health_check
from .update import cmd_update, update_project

__all__ = [
    "cmd_create",
    "create_project",
    "cmd_cleanup",
    "analyze_project",
    "cleanup_project",
    "cmd_migrate",
    "migrate_project",
    "cmd_health",
    "health_check",
    "cmd_update",
    "update_project",
]
