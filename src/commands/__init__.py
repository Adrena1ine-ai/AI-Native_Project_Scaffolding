"""
CLI Commands
"""

from .create import cmd_create, create_project
from .cleanup import cmd_cleanup, analyze_project, cleanup_project
from .migrate import cmd_migrate, migrate_project
from .health import cmd_health, health_check
from .update import cmd_update, update_project
from .review import cmd_review, review_changes, run_fox_scan, check_secrets
from .wizard import cmd_wizard, run_wizard
from .hooks import cmd_hooks, install_pre_commit_hook, check_hook_installed
from .pack import cmd_pack, pack_context
from .trace import cmd_trace, trace_file_dependencies
from .doctor import cmd_doctor, run_doctor, run_doctor_interactive
from .status import cmd_status, run_status_interactive

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
    "cmd_review",
    "review_changes",
    "run_fox_scan",
    "check_secrets",
    "cmd_wizard",
    "run_wizard",
    "cmd_hooks",
    "install_pre_commit_hook",
    "check_hook_installed",
    "cmd_pack",
    "pack_context",
    "cmd_trace",
    "trace_file_dependencies",
    "cmd_doctor",
    "run_doctor",
    "run_doctor_interactive",
    "cmd_status",
    "run_status_interactive",
]
