"""
Update command — update project to new Toolkit version
"""

from __future__ import annotations

from pathlib import Path

from ..core.constants import COLORS, VERSION


def update_project(project_path: Path) -> bool:
    """
    Update project to new Toolkit version
    """
    project_name = project_path.name
    
    version_file = project_path / ".toolkit-version"
    old_version = version_file.read_text().strip() if version_file.exists() else "unknown"
    
    if old_version == VERSION:
        print(f"{COLORS.info(f'Project already on latest version: {VERSION}')}")
        return True
    
    print(f"""
{COLORS.colorize('═' * 50, COLORS.CYAN)}
{COLORS.colorize(f'⬆️  Updating: {project_name}', COLORS.CYAN)}
{COLORS.colorize('═' * 50, COLORS.CYAN)}
   {old_version} → {VERSION}
""")
    
    # Update scripts
    from ..generators.scripts import (
        generate_bootstrap_sh,
        generate_health_check,
        generate_context_switcher,
    )
    
    print(f"\n{COLORS.colorize('📜 Updating scripts...', COLORS.CYAN)}")
    generate_bootstrap_sh(project_path, project_name)
    generate_health_check(project_path, project_name)
    generate_context_switcher(project_path)
    
    # Update CI if exists
    ci_file = project_path / ".github" / "workflows" / "ci.yml"
    if ci_file.exists():
        print(f"\n{COLORS.colorize('🚀 Updating CI...', COLORS.CYAN)}")
        from ..generators.ci_cd import generate_ci_workflow
        generate_ci_workflow(project_path, project_name)
    
    # Update pre-commit
    precommit_file = project_path / ".pre-commit-config.yaml"
    if precommit_file.exists():
        from ..generators.ci_cd import generate_pre_commit_config
        generate_pre_commit_config(project_path, project_name)
    
    # Update version
    version_file.write_text(VERSION)
    print(f"  {COLORS.success(f'.toolkit-version → {VERSION}')}")
    
    print(f"""
{COLORS.colorize('═' * 50, COLORS.GREEN)}
{COLORS.success('Update complete!')}
{COLORS.colorize('═' * 50, COLORS.GREEN)}
""")
    
    return True


def cmd_update() -> None:
    """Interactive update command"""
    print(COLORS.colorize("\n⬆️  PROJECT UPDATE\n", COLORS.GREEN))
    
    path_str = input("Project path: ").strip()
    if not path_str:
        print(COLORS.warning("Cancelled"))
        return
    
    path = Path(path_str).resolve()
    if not path.exists():
        print(COLORS.error(f"Path does not exist: {path}"))
        return
    
    version_file = path / ".toolkit-version"
    if not version_file.exists():
        print(COLORS.warning("This is not a Toolkit project (no .toolkit-version)"))
        confirm = input("Continue with migration? (y/N): ").strip().lower()
        if confirm != 'y':
            return
        from .migrate import migrate_project
        migrate_project(path)
        return
    
    old_version = version_file.read_text().strip()
    
    if old_version == VERSION:
        print(COLORS.info(f"Already on latest version: {VERSION}"))
        return
    
    print(f"  Current: {old_version}")
    print(f"  New: {VERSION}")
    
    confirm = input("\nUpdate? (Y/n): ").strip().lower()
    if confirm == 'n':
        print(COLORS.warning("Cancelled"))
        return
    
    update_project(path)
