"""
Команда migrate — добавление Toolkit в существующий проект
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
    Добавить Toolkit в существующий проект
    
    Args:
        project_path: Путь к проекту
        ai_targets: Список AI
        include_ci: Добавить CI/CD
        quiet: Тихий режим
    """
    if ai_targets is None:
        ai_targets = get_default_ai_targets()
    
    project_name = project_path.name
    date = datetime.now().strftime("%Y-%m-%d")
    
    if not quiet:
        print(f"""
{COLORS.colorize('═' * 50, COLORS.CYAN)}
{COLORS.colorize(f'📦 Migrating: {project_name}', COLORS.CYAN)}
{COLORS.colorize('═' * 50, COLORS.CYAN)}
""")
    
    # AI конфиги (если не существуют)
    if not (project_path / "_AI_INCLUDE").exists():
        generate_ai_configs(project_path, project_name, ai_targets, date)
    else:
        if not quiet:
            print(f"  {COLORS.warning('_AI_INCLUDE/ уже существует, пропускаю')}")
    
    # Scripts
    if not (project_path / "scripts" / "bootstrap.sh").exists():
        generate_scripts(project_path, project_name)
    else:
        if not quiet:
            print(f"  {COLORS.warning('scripts/ уже существуют, пропускаю')}")
    
    # CI/CD
    if include_ci and not (project_path / ".github" / "workflows").exists():
        generate_ci_files(project_path, project_name)
    
    # .toolkit-version
    from ..core.constants import VERSION
    (project_path / ".toolkit-version").write_text(VERSION)
    
    if not quiet:
        print(f"""
{COLORS.colorize('═' * 50, COLORS.GREEN)}
{COLORS.success('Миграция завершена!')}
{COLORS.colorize('═' * 50, COLORS.GREEN)}
""")
    
    return True


def cmd_migrate() -> None:
    """Интерактивная команда миграции"""
    print(COLORS.colorize("\n📦 МИГРАЦИЯ ПРОЕКТА\n", COLORS.GREEN))
    
    path_str = input("Путь к проекту: ").strip()
    if not path_str:
        print(COLORS.warning("Отменено"))
        return
    
    path = Path(path_str).resolve()
    if not path.exists():
        print(COLORS.error(f"Путь не существует: {path}"))
        return
    
    ai_targets = get_default_ai_targets()
    print(f"\n  AI: {', '.join(ai_targets)}")
    
    confirm = input(f"\nДобавить Toolkit в {path.name}? (Y/n): ").strip().lower()
    if confirm == 'n':
        print(COLORS.warning("Отменено"))
        return
    
    migrate_project(path, ai_targets)
