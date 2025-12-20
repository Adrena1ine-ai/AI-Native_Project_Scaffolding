"""
Команда health — проверка здоровья проекта
"""

from __future__ import annotations

from pathlib import Path

from ..core.constants import COLORS, VERSION


def health_check(project_path: Path) -> bool:
    """
    Проверить здоровье проекта
    
    Returns:
        True если все проверки пройдены
    """
    project_name = project_path.name
    
    print(f"""
{COLORS.colorize('═' * 50, COLORS.CYAN)}
{COLORS.colorize(f'🏥 Health Check: {project_name}', COLORS.CYAN)}
{COLORS.colorize('═' * 50, COLORS.CYAN)}
""")
    
    errors = 0
    warnings = 0
    
    # 1. Venv
    print(f"{COLORS.colorize('📍 Virtual Environment', COLORS.BOLD)}")
    venv_path = project_path.parent / "_venvs" / f"{project_name}-venv"
    
    if venv_path.exists():
        print(f"   {COLORS.success(f'Venv: {venv_path}')}")
    else:
        print(f"   {COLORS.error(f'Venv не найден: {venv_path}')}")
        errors += 1
    
    for bad in ["venv", ".venv", "env"]:
        if (project_path / bad).is_dir():
            print(f"   {COLORS.error(f'ЗАПРЕЩЕНО: {bad}/ в проекте!')}")
            errors += 1
    
    # 2. Конфигурация
    print(f"\n{COLORS.colorize('📍 Configuration', COLORS.BOLD)}")
    
    if (project_path / ".env").exists():
        print(f"   {COLORS.success('.env')}")
    else:
        print(f"   {COLORS.warning('.env отсутствует')}")
        warnings += 1
    
    if (project_path / "requirements.txt").exists():
        print(f"   {COLORS.success('requirements.txt')}")
    else:
        print(f"   {COLORS.warning('requirements.txt отсутствует')}")
        warnings += 1
    
    # 3. AI конфиги
    print(f"\n{COLORS.colorize('📍 AI Configuration', COLORS.BOLD)}")
    
    if (project_path / "_AI_INCLUDE").exists():
        print(f"   {COLORS.success('_AI_INCLUDE/')}")
    else:
        print(f"   {COLORS.error('_AI_INCLUDE/ отсутствует')}")
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
    print(f"\n{COLORS.colorize('📍 Scripts', COLORS.BOLD)}")
    
    scripts = ["bootstrap.sh", "health_check.sh", "context.py"]
    for script in scripts:
        if (project_path / "scripts" / script).exists():
            print(f"   {COLORS.success(script)}")
        else:
            print(f"   {COLORS.warning(f'{script} отсутствует')}")
            warnings += 1
    
    # 5. Docker
    print(f"\n{COLORS.colorize('📍 Docker', COLORS.BOLD)}")
    
    if (project_path / "Dockerfile").exists():
        print(f"   {COLORS.success('Dockerfile')}")
    else:
        print(f"   {COLORS.info('Dockerfile отсутствует')}")
    
    if (project_path / "docker-compose.yml").exists():
        print(f"   {COLORS.success('docker-compose.yml')}")
    
    # 6. CI/CD
    print(f"\n{COLORS.colorize('📍 CI/CD', COLORS.BOLD)}")
    
    if (project_path / ".github" / "workflows" / "ci.yml").exists():
        print(f"   {COLORS.success('GitHub Actions')}")
    else:
        print(f"   {COLORS.info('CI не настроен')}")
    
    # 7. Git
    print(f"\n{COLORS.colorize('📍 Git', COLORS.BOLD)}")
    
    if (project_path / ".git").exists():
        print(f"   {COLORS.success('Git репозиторий')}")
    else:
        print(f"   {COLORS.warning('Не git репозиторий')}")
        warnings += 1
    
    # 8. Toolkit version
    print(f"\n{COLORS.colorize('📍 Toolkit', COLORS.BOLD)}")
    
    version_file = project_path / ".toolkit-version"
    if version_file.exists():
        version = version_file.read_text().strip()
        if version == VERSION:
            print(f"   {COLORS.success(f'Версия: {version}')}")
        else:
            print(f"   {COLORS.warning(f'Версия {version} → доступна {VERSION}')}")
            warnings += 1
    else:
        print(f"   {COLORS.warning('Версия не указана')}")
        warnings += 1
    
    # Итог
    print(f"""
{COLORS.colorize('═' * 50, COLORS.CYAN)}""")
    
    if errors == 0 and warnings == 0:
        print(f"{COLORS.success('Все проверки пройдены!')}")
        return True
    elif errors == 0:
        print(f"{COLORS.warning(f'{warnings} предупреждений')}")
        return True
    else:
        print(f"{COLORS.error(f'{errors} ошибок, {warnings} предупреждений')}")
        return False


def cmd_health() -> None:
    """Интерактивная команда health check"""
    print(COLORS.colorize("\n🏥 HEALTH CHECK\n", COLORS.GREEN))
    
    path_str = input("Путь к проекту: ").strip()
    if not path_str:
        print(COLORS.warning("Отменено"))
        return
    
    path = Path(path_str).resolve()
    if not path.exists():
        print(COLORS.error(f"Путь не существует: {path}"))
        return
    
    health_check(path)
