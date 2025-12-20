"""
Команда cleanup — очистка грязных проектов
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
    """Найденная проблема"""
    type: str
    severity: str  # error, warning, info
    path: Path | None
    size_mb: float
    message: str
    fix_action: str
    
    def __str__(self) -> str:
        icons = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}
        size = f" ({self.size_mb:.1f} MB)" if self.size_mb > 0 else ""
        return f"{icons.get(self.severity, '•')} {self.message}{size}"


def analyze_project(project_path: Path) -> list[Issue]:
    """Анализировать проект на проблемы"""
    issues: list[Issue] = []
    
    # 1. venv внутри проекта
    for venv_name in ["venv", ".venv", "env"]:
        venv_path = project_path / venv_name
        if venv_path.is_dir() and (venv_path / "bin").exists():
            size = get_dir_size(venv_path)
            issues.append(Issue(
                type="venv",
                severity="error",
                path=venv_path,
                size_mb=size,
                message=f"Найден {venv_name}/ внутри проекта",
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
                message="Найден site-packages/",
                fix_action="delete"
            ))
    
    # 3. Большие логи
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
                    message=f"Большой лог: {log_file.name}",
                    fix_action="truncate:1000"
                ))
    
    # 4. Большие данные
    data_dir = project_path / "data"
    if data_dir.exists():
        size = get_dir_size(data_dir)
        if size > 100:
            issues.append(Issue(
                type="data",
                severity="warning",
                path=data_dir,
                size_mb=size,
                message="Большая папка data/",
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
            message=f"Найдено {pycache_count} папок __pycache__",
            fix_action="delete_all"
        ))
    
    # 6. Отсутствующие конфиги
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
            message=f"Отсутствуют: {', '.join(missing)}",
            fix_action="create"
        ))
    
    return issues


def select_cleanup_level() -> str:
    """Выбор уровня очистки"""
    print("\n🧹 Выбери уровень очистки:\n")
    
    levels = list(CLEANUP_LEVELS.items())
    for i, (name, level) in enumerate(levels, 1):
        print(f"  {i}. {level['name']} — {level['description']}")
    
    while True:
        choice = input(f"\nВыбор (1-{len(levels)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(levels):
                return levels[idx][0]
        except ValueError:
            pass
        print("  Неверный выбор")


def create_backup(project_path: Path) -> Path:
    """Создать бэкап"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{project_path.name}_backup_{timestamp}.tar.gz"
    backup_path = project_path.parent / backup_name
    
    print(f"\n{COLORS.colorize(f'📦 Создаю бэкап: {backup_name}', COLORS.CYAN)}")
    
    with tarfile.open(backup_path, "w:gz") as tar:
        tar.add(project_path, arcname=project_path.name)
    
    size = backup_path.stat().st_size / (1024 * 1024)
    print(f"  {COLORS.success(f'Бэкап создан ({size:.1f} MB)')}")
    
    return backup_path


def cleanup_project(project_path: Path, level: str) -> bool:
    """Выполнить очистку"""
    level_config = CLEANUP_LEVELS.get(level)
    if not level_config:
        print(COLORS.error(f"Неизвестный уровень: {level}"))
        return False
    
    actions = level_config["actions"]
    
    print(f"\n{COLORS.colorize(f'🧹 Очистка: {project_path.name}', COLORS.CYAN)}")
    print(f"   Уровень: {level_config['name']}")
    
    # Safe — только анализ
    if level == "safe":
        print(f"\n{COLORS.warning('Режим safe — без изменений')}")
        return True
    
    # Бэкап
    if "backup" in actions:
        create_backup(project_path)
    
    freed_mb = 0.0
    
    # Перемещение venv
    if "move_venv" in actions:
        for venv_name in ["venv", ".venv", "env"]:
            venv_path = project_path / venv_name
            if venv_path.is_dir() and (venv_path / "bin").exists():
                size = get_dir_size(venv_path)
                venvs_dir = project_path.parent / "_venvs"
                venvs_dir.mkdir(exist_ok=True)
                new_path = venvs_dir / f"{project_path.name}-venv"
                
                if new_path.exists():
                    print(f"  {COLORS.warning(f'{new_path} существует, удаляю старый venv')}")
                    shutil.rmtree(venv_path)
                else:
                    print(f"  {COLORS.colorize(f'Перемещаю {venv_name}/ → {new_path}', COLORS.CYAN)}")
                    shutil.move(str(venv_path), str(new_path))
                
                freed_mb += size
    
    # Удаление __pycache__
    for pycache in project_path.rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)
    
    # Очистка логов
    if "move_data" in actions:
        logs_dir = project_path / "logs"
        if logs_dir.exists():
            for log_file in logs_dir.glob("*.log"):
                size = log_file.stat().st_size / (1024 * 1024)
                if size > 10:
                    lines = log_file.read_text(errors="ignore").splitlines()
                    log_file.write_text("\n".join(lines[-1000:]))
                    print(f"  {COLORS.colorize(f'Очищен {log_file.name}', COLORS.CYAN)}")
                    freed_mb += size * 0.9
    
    # Создание конфигов
    if "create_configs" in actions:
        from .migrate import migrate_project
        print(f"\n{COLORS.colorize('📄 Создаю конфиги...', COLORS.CYAN)}")
        migrate_project(project_path, ["cursor", "copilot", "claude"], quiet=True)
    
    print(f"""
{COLORS.colorize('═' * 50, COLORS.GREEN)}
{COLORS.success('Очистка завершена!')}
{COLORS.colorize('═' * 50, COLORS.GREEN)}
   Освобождено: ~{freed_mb:.1f} MB
""")
    
    return True


def cmd_cleanup() -> None:
    """Интерактивная команда очистки"""
    print(COLORS.colorize("\n🧹 ОЧИСТКА ПРОЕКТА\n", COLORS.GREEN))
    
    path_str = input("Путь к проекту: ").strip()
    if not path_str:
        print(COLORS.warning("Отменено"))
        return
    
    path = Path(path_str).resolve()
    if not path.exists():
        print(COLORS.error(f"Путь не существует: {path}"))
        return
    
    # Анализ
    print(f"\n{COLORS.colorize('🔍 Анализирую...', COLORS.CYAN)}\n")
    issues = analyze_project(path)
    
    if not issues:
        print(COLORS.success("Проект чистый! Проблем не найдено."))
        return
    
    # Показать проблемы
    print(f"{COLORS.colorize('Найдены проблемы:', COLORS.RED)}\n")
    for issue in issues:
        print(f"   {issue}")
    
    # Выбор уровня
    level = select_cleanup_level()
    
    if level == "safe":
        print(f"\n{COLORS.warning('Режим safe — только рекомендации')}")
        return
    
    # Подтверждение
    confirm = input(f"\nВыполнить очистку '{level}'? (y/N): ").strip().lower()
    if confirm != 'y':
        print(COLORS.warning("Отменено"))
        return
    
    cleanup_project(path, level)
