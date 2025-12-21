"""
Health command - check project health
"""

from __future__ import annotations

from pathlib import Path

from ..core.constants import COLORS, VERSION


def health_check(project_path: Path) -> bool:
    """
    Check project health
    
    Returns:
        True if all checks passed
    """
    project_name = project_path.name
    
    print(f"""
{COLORS.colorize('=' * 50, COLORS.CYAN)}
{COLORS.colorize(f'Health Check: {project_name}', COLORS.CYAN)}
{COLORS.colorize('=' * 50, COLORS.CYAN)}
""")
    
    errors = 0
    warnings = 0
    
    # 1. Venv
    print(f"{COLORS.colorize('Virtual Environment', COLORS.BOLD)}")
    venv_path = project_path.parent / "_venvs" / f"{project_name}-venv"
    
    if venv_path.exists():
        print(f"   {COLORS.success(f'Venv: {venv_path}')}")
    else:
        print(f"   {COLORS.error(f'Venv not found: {venv_path}')}")
        errors += 1
    
    for bad in ["venv", ".venv", "env"]:
        if (project_path / bad).is_dir():
            print(f"   {COLORS.error(f'FORBIDDEN: {bad}/ in project!')}")
            errors += 1
    
    # 2. Configuration
    print(f"\n{COLORS.colorize('Configuration', COLORS.BOLD)}")
    
    if (project_path / ".env").exists():
        print(f"   {COLORS.success('.env')}")
    else:
        print(f"   {COLORS.warning('.env missing')}")
        warnings += 1
    
    if (project_path / "requirements.txt").exists():
        print(f"   {COLORS.success('requirements.txt')}")
    else:
        print(f"   {COLORS.warning('requirements.txt missing')}")
        warnings += 1
    
    # 3. AI configs
    print(f"\n{COLORS.colorize('AI Configuration', COLORS.BOLD)}")
    
    if (project_path / "_AI_INCLUDE").exists():
        print(f"   {COLORS.success('_AI_INCLUDE/')}")
    else:
        print(f"   {COLORS.error('_AI_INCLUDE/ missing')}")
        errors += 1
    
    ai_files = [
        (".cursorrules", "Cursor"),
        (".cursorignore", "Cursor Ignore"),
        (".github/copilot-instructions.md", "Copilot"),
        ("CLAUDE.md", "Claude"),
    ]
    
    for file, name in ai_files:
        if (project_path / file).exists():
            print(f"   {COLORS.success(name)}")
    
    # 4. Scripts
    print(f"\n{COLORS.colorize('Scripts', COLORS.BOLD)}")
    
    scripts = ["bootstrap.sh", "health_check.sh", "context.py"]
    for script in scripts:
        if (project_path / "scripts" / script).exists():
            print(f"   {COLORS.success(script)}")
        else:
            print(f"   {COLORS.warning(f'{script} missing')}")
            warnings += 1
    
    # 5. Docker
    print(f"\n{COLORS.colorize('Docker', COLORS.BOLD)}")
    
    if (project_path / "Dockerfile").exists():
        print(f"   {COLORS.success('Dockerfile')}")
    else:
        print(f"   {COLORS.info('Dockerfile missing')}")
    
    if (project_path / "docker-compose.yml").exists():
        print(f"   {COLORS.success('docker-compose.yml')}")
    
    # 6. CI/CD
    print(f"\n{COLORS.colorize('CI/CD', COLORS.BOLD)}")
    
    if (project_path / ".github" / "workflows" / "ci.yml").exists():
        print(f"   {COLORS.success('GitHub Actions')}")
    else:
        print(f"   {COLORS.info('CI not configured')}")
    
    # 7. Git
    print(f"\n{COLORS.colorize('Git', COLORS.BOLD)}")
    
    if (project_path / ".git").exists():
        print(f"   {COLORS.success('Git repository')}")
    else:
        print(f"   {COLORS.warning('Not a git repository')}")
        warnings += 1
    
    # 8. Toolkit version
    print(f"\n{COLORS.colorize('Toolkit', COLORS.BOLD)}")
    
    version_file = project_path / ".toolkit-version"
    if version_file.exists():
        version = version_file.read_text().strip()
        if version == VERSION:
            print(f"   {COLORS.success(f'Version: {version}')}")
        else:
            print(f"   {COLORS.warning(f'Version {version} -> available {VERSION}')}")
            warnings += 1
    else:
        print(f"   {COLORS.warning('Version not specified')}")
        warnings += 1
    
    # Summary
    print(f"""
{COLORS.colorize('=' * 50, COLORS.CYAN)}""")
    
    if errors == 0 and warnings == 0:
        print(f"{COLORS.success('All checks passed!')}")
        return True
    elif errors == 0:
        print(f"{COLORS.warning(f'{warnings} warnings')}")
        return True
    else:
        print(f"{COLORS.error(f'{errors} errors, {warnings} warnings')}")
        return False


def cmd_health() -> None:
    """Interactive health check command"""
    print(COLORS.colorize("\nHEALTH CHECK\n", COLORS.GREEN))
    
    path_str = input("Project path: ").strip()
    if not path_str:
        print(COLORS.warning("Cancelled"))
        return
    
    path = Path(path_str).resolve()
    if not path.exists():
        print(COLORS.error(f"Path does not exist: {path}"))
        return
    
    health_check(path)
