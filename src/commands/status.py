"""
Status command — Regenerate PROJECT_STATUS.md from current codebase.
"""

from __future__ import annotations

from pathlib import Path

from ..utils.status_generator import update_status, generate_status_md
from ..core.constants import COLORS


def cmd_status(args=None) -> bool:
    """Regenerate PROJECT_STATUS.md from current codebase state."""
    # Get project path
    if args and hasattr(args, 'path') and args.path:
        project_path = Path(args.path).resolve()
    else:
        project_path = Path.cwd()
    
    if not project_path.exists():
        print(COLORS.error(f"Path not found: {project_path}"))
        return False
    
    print(COLORS.info(f"Scanning project: {project_path.name}"))
    
    # Check for src directory
    if not (project_path / "src").exists():
        print(COLORS.warning("No src/ directory found. Scanning anyway..."))
    
    # Skip tests if requested
    skip_tests = args and hasattr(args, 'skip_tests') and args.skip_tests
    
    try:
        status_file = update_status(project_path, skip_tests=skip_tests)
        print(COLORS.success(f"Generated: {status_file}"))
        
        # Show preview if requested
        if args and hasattr(args, 'preview') and args.preview:
            print()
            print("─" * 60)
            print(generate_status_md(project_path, skip_tests=True))
            print("─" * 60)
        
        return True
        
    except Exception as e:
        print(COLORS.error(f"Error generating status: {e}"))
        return False


def run_status_interactive() -> None:
    """Interactive status command for menu."""
    print(COLORS.colorize("\n📊 GENERATE PROJECT STATUS\n", COLORS.GREEN))
    
    path_str = input("Project path (Enter = current folder): ").strip()
    if not path_str:
        path_str = "."
    
    project_path = Path(path_str).resolve()
    if not project_path.exists():
        print(COLORS.error(f"Path does not exist: {project_path}"))
        return
    
    skip_tests = input("Skip tests? (Y/n): ").strip().lower() != 'n'
    preview = input("Preview output? (y/N): ").strip().lower() == 'y'
    
    class Args:
        pass
    
    args = Args()
    args.path = project_path
    args.skip_tests = skip_tests
    args.preview = preview
    
    cmd_status(args)

