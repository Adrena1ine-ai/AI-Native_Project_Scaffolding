"""
Команда update — обновление проекта до новой версии Toolkit
"""

from __future__ import annotations

from pathlib import Path

from ..core.constants import COLORS, VERSION


def update_project(project_path: Path) -> bool:
    """
    Обновить проект до новой версии Toolkit
    """
    project_name = project_path.name
    
    version_file = project_path / ".toolkit-version"
    old_version = version_file.read_text().strip() if version_file.exists() else "unknown"
    
    if old_version == VERSION:
        print(f"{COLORS.info(f'Проект уже на последней версии: {VERSION}')}")
        return True
    
    print(f"""
{COLORS.colorize('═' * 50, COLORS.CYAN)}
{COLORS.colorize(f'⬆️  Updating: {project_name}', COLORS.CYAN)}
{COLORS.colorize('═' * 50, COLORS.CYAN)}
   {old_version} → {VERSION}
""")
    
    # Обновляем scripts
    from ..generators.scripts import (
        generate_bootstrap_sh,
        generate_health_check,
        generate_context_switcher,
    )
    
    print(f"\n{COLORS.colorize('📜 Обновляю scripts...', COLORS.CYAN)}")
    generate_bootstrap_sh(project_path, project_name)
    generate_health_check(project_path, project_name)
    generate_context_switcher(project_path)
    
    # Обновляем CI если есть
    ci_file = project_path / ".github" / "workflows" / "ci.yml"
    if ci_file.exists():
        print(f"\n{COLORS.colorize('🚀 Обновляю CI...', COLORS.CYAN)}")
        from ..generators.ci_cd import generate_ci_workflow
        generate_ci_workflow(project_path, project_name)
    
    # Обновляем pre-commit
    precommit_file = project_path / ".pre-commit-config.yaml"
    if precommit_file.exists():
        from ..generators.ci_cd import generate_pre_commit_config
        generate_pre_commit_config(project_path, project_name)
    
    # Обновляем версию
    version_file.write_text(VERSION)
    print(f"  {COLORS.success(f'.toolkit-version → {VERSION}')}")
    
    print(f"""
{COLORS.colorize('═' * 50, COLORS.GREEN)}
{COLORS.success('Обновление завершено!')}
{COLORS.colorize('═' * 50, COLORS.GREEN)}
""")
    
    return True


def cmd_update() -> None:
    """Интерактивная команда обновления"""
    print(COLORS.colorize("\n⬆️  ОБНОВЛЕНИЕ ПРОЕКТА\n", COLORS.GREEN))
    
    path_str = input("Путь к проекту: ").strip()
    if not path_str:
        print(COLORS.warning("Отменено"))
        return
    
    path = Path(path_str).resolve()
    if not path.exists():
        print(COLORS.error(f"Путь не существует: {path}"))
        return
    
    version_file = path / ".toolkit-version"
    if not version_file.exists():
        print(COLORS.warning("Это не Toolkit проект (нет .toolkit-version)"))
        confirm = input("Продолжить миграцию? (y/N): ").strip().lower()
        if confirm != 'y':
            return
        from .migrate import migrate_project
        migrate_project(path)
        return
    
    old_version = version_file.read_text().strip()
    
    if old_version == VERSION:
        print(COLORS.info(f"Уже на последней версии: {VERSION}"))
        return
    
    print(f"  Текущая: {old_version}")
    print(f"  Новая: {VERSION}")
    
    confirm = input("\nОбновить? (Y/n): ").strip().lower()
    if confirm == 'n':
        print(COLORS.warning("Отменено"))
        return
    
    update_project(path)
