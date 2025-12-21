"""
Cleanup command - clean dirty projects
"""

from __future__ import annotations

import shutil
import tarfile
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

from ..core.constants import COLORS, CLEANUP_LEVELS
from ..core.file_utils import get_dir_size


@dataclass
class Issue:
    """Found issue"""
    type: str
    severity: str  # error, warning, info
    path: Path | None
    size_mb: float
    message: str
    fix_action: str
    
    def __str__(self) -> str:
        icons = {"error": "[ERROR]", "warning": "[WARN]", "info": "[INFO]"}
        size = f" ({self.size_mb:.1f} MB)" if self.size_mb > 0 else ""
        return f"{icons.get(self.severity, '*')} {self.message}{size}"


def analyze_project(project_path: Path) -> list[Issue]:
    """Analyze project for issues"""
    issues: list[Issue] = []
    
    # 1. venv inside project
    for venv_name in ["venv", ".venv", "env"]:
        venv_path = project_path / venv_name
        if venv_path.is_dir() and (venv_path / "bin").exists():
            size = get_dir_size(venv_path)
            issues.append(Issue(
                type="venv",
                severity="error",
                path=venv_path,
                size_mb=size,
                message=f"Found {venv_name}/ inside project",
                fix_action=f"move:../_venvs/{project_path.name}-venv"
            ))
    
    # 2. site-packages
    for sp in project_path.rglob("site-packages"):
        if sp.is_dir():
            size = get_dir_size(sp)
            issues.append(Issue(
                type="venv",
                severity="error",
                path=sp,
                size_mb=size,
                message="Found site-packages/",
                fix_action="delete"
            ))
    
    # 3. Large logs
    logs_dir = project_path / "logs"
    if logs_dir.exists():
        for log_file in logs_dir.glob("*.log"):
            size = log_file.stat().st_size / (1024 * 1024)
            if size > 10:
                issues.append(Issue(
                    type="logs",
                    severity="warning",
                    path=log_file,
                    size_mb=size,
                    message=f"Large log: {log_file.name}",
                    fix_action="truncate:1000"
                ))
    
    # 4. Large data
    data_dir = project_path / "data"
    if data_dir.exists():
        size = get_dir_size(data_dir)
        if size > 100:
            issues.append(Issue(
                type="data",
                severity="warning",
                path=data_dir,
                size_mb=size,
                message="Large data/ folder",
                fix_action=f"move:../_data/{project_path.name}"
            ))
    
    # 5. __pycache__
    pycache_count = len(list(project_path.rglob("__pycache__")))
    if pycache_count > 0:
        issues.append(Issue(
            type="cache",
            severity="info",
            path=None,
            size_mb=0,
            message=f"Found {pycache_count} __pycache__ folders",
            fix_action="delete_all"
        ))
    
    # 6. Missing configs
    missing = []
    if not (project_path / ".cursorignore").exists():
        missing.append(".cursorignore")
    if not (project_path / "_AI_INCLUDE").exists():
        missing.append("_AI_INCLUDE/")
    if not (project_path / "scripts" / "bootstrap.sh").exists():
        missing.append("scripts/bootstrap.sh")
    
    if missing:
        issues.append(Issue(
            type="config",
            severity="warning",
            path=None,
            size_mb=0,
            message=f"Missing: {', '.join(missing)}",
            fix_action="create"
        ))
    
    return issues


def select_cleanup_level() -> str:
    """Select cleanup level"""
    print("\nSelect cleanup level:\n")
    
    levels = list(CLEANUP_LEVELS.items())
    for i, (name, level) in enumerate(levels, 1):
        print(f"  {i}. {level['name']} - {level['description']}")
    
    while True:
        choice = input(f"\nChoice (1-{len(levels)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(levels):
                return levels[idx][0]
        except ValueError:
            pass
        print("  Invalid choice")


def create_backup(project_path: Path) -> Path:
    """Create backup"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{project_path.name}_backup_{timestamp}.tar.gz"
    backup_path = project_path.parent / backup_name
    
    print(f"\n{COLORS.colorize(f'Creating backup: {backup_name}', COLORS.CYAN)}")
    
    with tarfile.open(backup_path, "w:gz") as tar:
        tar.add(project_path, arcname=project_path.name)
    
    size = backup_path.stat().st_size / (1024 * 1024)
    print(f"  {COLORS.success(f'Backup created ({size:.1f} MB)')}")
    
    return backup_path


def cleanup_project(project_path: Path, level: str) -> bool:
    """Run cleanup"""
    level_config = CLEANUP_LEVELS.get(level)
    if not level_config:
        print(COLORS.error(f"Unknown level: {level}"))
        return False
    
    actions = level_config["actions"]
    
    print(f"\n{COLORS.colorize(f'Cleanup: {project_path.name}', COLORS.CYAN)}")
    print(f"   Level: {level_config['name']}")
    
    # Safe - analysis only
    if level == "safe":
        print(f"\n{COLORS.warning('Safe mode - no changes')}")
        return True
    
    # Backup
    if "backup" in actions:
        create_backup(project_path)
    
    freed_mb = 0.0
    
    # Move venv
    if "move_venv" in actions:
        for venv_name in ["venv", ".venv", "env"]:
            venv_path = project_path / venv_name
            if venv_path.is_dir() and (venv_path / "bin").exists():
                size = get_dir_size(venv_path)
                venvs_dir = project_path.parent / "_venvs"
                venvs_dir.mkdir(exist_ok=True)
                new_path = venvs_dir / f"{project_path.name}-venv"
                
                if new_path.exists():
                    print(f"  {COLORS.warning(f'{new_path} exists, deleting old venv')}")
                    shutil.rmtree(venv_path)
                else:
                    print(f"  {COLORS.colorize(f'Moving {venv_name}/ -> {new_path}', COLORS.CYAN)}")
                    shutil.move(str(venv_path), str(new_path))
                
                freed_mb += size
    
    # Delete __pycache__
    for pycache in project_path.rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)
    
    # Clean logs
    if "move_data" in actions:
        logs_dir = project_path / "logs"
        if logs_dir.exists():
            for log_file in logs_dir.glob("*.log"):
                size = log_file.stat().st_size / (1024 * 1024)
                if size > 10:
                    lines = log_file.read_text(errors="ignore").splitlines()
                    log_file.write_text("\n".join(lines[-1000:]))
                    print(f"  {COLORS.colorize(f'Cleaned {log_file.name}', COLORS.CYAN)}")
                    freed_mb += size * 0.9
    
    # Create configs
    if "create_configs" in actions:
        from .migrate import migrate_project
        print(f"\n{COLORS.colorize('Creating configs...', COLORS.CYAN)}")
        migrate_project(project_path, ["cursor", "copilot", "claude"], quiet=True)
    
    print(f"""
{COLORS.colorize('=' * 50, COLORS.GREEN)}
{COLORS.success('Cleanup complete!')}
{COLORS.colorize('=' * 50, COLORS.GREEN)}
   Freed: ~{freed_mb:.1f} MB
""")
    
    return True


def cmd_cleanup() -> None:
    """Interactive cleanup command"""
    print(COLORS.colorize("\nCLEANUP PROJECT\n", COLORS.GREEN))
    
    path_str = input("Project path: ").strip()
    if not path_str:
        print(COLORS.warning("Cancelled"))
        return
    
    path = Path(path_str).resolve()
    if not path.exists():
        print(COLORS.error(f"Path does not exist: {path}"))
        return
    
    # Analyze
    print(f"\n{COLORS.colorize('Analyzing...', COLORS.CYAN)}\n")
    issues = analyze_project(path)
    
    if not issues:
        print(COLORS.success("Project is clean! No issues found."))
        return
    
    # Show issues
    print(f"{COLORS.colorize('Issues found:', COLORS.RED)}\n")
    for issue in issues:
        print(f"   {issue}")
    
    # Select level
    level = select_cleanup_level()
    
    if level == "safe":
        print(f"\n{COLORS.warning('Safe mode - recommendations only')}")
        return
    
    # Confirm
    confirm = input(f"\nRun cleanup '{level}'? (y/N): ").strip().lower()
    if confirm != 'y':
        print(COLORS.warning("Cancelled"))
        return
    
    cleanup_project(path, level)
