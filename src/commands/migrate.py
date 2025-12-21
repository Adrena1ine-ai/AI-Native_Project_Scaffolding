"""
Migrate command - add Toolkit to existing project
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime

from ..core.constants import COLORS
from ..core.config import get_default_ai_targets

from ..generators import (
    generate_ai_configs,
    generate_scripts,
    generate_ci_files,
)


def migrate_project(
    project_path: Path,
    ai_targets: list[str] = None,
    include_ci: bool = True,
    quiet: bool = False,
) -> bool:
    """
    Add Toolkit to existing project
    
    Args:
        project_path: Project path
        ai_targets: AI list
        include_ci: Add CI/CD
        quiet: Quiet mode
    """
    if ai_targets is None:
        ai_targets = get_default_ai_targets()
    
    project_name = project_path.name
    date = datetime.now().strftime("%Y-%m-%d")
    
    if not quiet:
        print(f"""
{COLORS.colorize('=' * 50, COLORS.CYAN)}
{COLORS.colorize(f'Migrating: {project_name}', COLORS.CYAN)}
{COLORS.colorize('=' * 50, COLORS.CYAN)}
""")
    
    # AI configs (if not exist)
    if not (project_path / "_AI_INCLUDE").exists():
        generate_ai_configs(project_path, project_name, ai_targets, date)
    else:
        if not quiet:
            print(f"  {COLORS.warning('_AI_INCLUDE/ already exists, skipping')}")
    
    # Scripts
    if not (project_path / "scripts" / "bootstrap.sh").exists():
        generate_scripts(project_path, project_name)
    else:
        if not quiet:
            print(f"  {COLORS.warning('scripts/ already exist, skipping')}")
    
    # CI/CD
    if include_ci and not (project_path / ".github" / "workflows").exists():
        generate_ci_files(project_path, project_name)
    
    # .toolkit-version
    from ..core.constants import VERSION
    (project_path / ".toolkit-version").write_text(VERSION)
    
    if not quiet:
        print(f"""
{COLORS.colorize('=' * 50, COLORS.GREEN)}
{COLORS.success('Migration complete!')}
{COLORS.colorize('=' * 50, COLORS.GREEN)}
""")
    
    return True


def cmd_migrate() -> None:
    """Interactive migrate command"""
    print(COLORS.colorize("\nMIGRATE PROJECT\n", COLORS.GREEN))
    
    path_str = input("Project path: ").strip()
    if not path_str:
        print(COLORS.warning("Cancelled"))
        return
    
    path = Path(path_str).resolve()
    if not path.exists():
        print(COLORS.error(f"Path does not exist: {path}"))
        return
    
    ai_targets = get_default_ai_targets()
    print(f"\n  AI: {', '.join(ai_targets)}")
    
    confirm = input(f"\nAdd Toolkit to {path.name}? (Y/n): ").strip().lower()
    if confirm == 'n':
        print(COLORS.warning("Cancelled"))
        return
    
    migrate_project(path, ai_targets)
