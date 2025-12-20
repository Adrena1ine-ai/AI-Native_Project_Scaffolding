"""
Утилиты для работы с файлами
"""

from __future__ import annotations

import os
import stat
import shutil
from pathlib import Path
from typing import Optional
from string import Template

from .constants import COLORS


def create_file(
    path: Path, 
    content: str, 
    executable: bool = False,
    quiet: bool = False
) -> None:
    """
    Создать файл с содержимым
    
    Args:
        path: Путь к файлу
        content: Содержимое
        executable: Сделать исполняемым
        quiet: Не выводить сообщение
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    
    if executable:
        make_executable(path)
    
    if not quiet:
        rel_path = path.name if len(str(path)) > 50 else path
        print(f"  {COLORS.success(str(rel_path))}")


def make_executable(path: Path) -> None:
    """Сделать файл исполняемым"""
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def copy_template(
    src: Path, 
    dst: Path, 
    context: dict,
    executable: bool = False
) -> None:
    """
    Скопировать шаблон с подстановкой переменных
    
    Args:
        src: Исходный файл шаблона
        dst: Целевой путь
        context: Словарь переменных для подстановки
        executable: Сделать исполняемым
    """
    if not src.exists():
        return
    
    content = src.read_text(encoding="utf-8")
    
    # Подстановка переменных {{variable}}
    for key, value in context.items():
        content = content.replace(f"{{{{{key}}}}}", str(value))
        content = content.replace(f"{{{key}}}", str(value))
    
    create_file(dst, content, executable=executable)


def get_dir_size(path: Path) -> float:
    """Получить размер директории в MB"""
    total = 0
    try:
        for p in path.rglob("*"):
            if p.is_file():
                total += p.stat().st_size
    except (PermissionError, OSError):
        pass
    return total / (1024 * 1024)


def remove_dir(path: Path) -> bool:
    """Безопасно удалить директорию"""
    try:
        if path.exists():
            shutil.rmtree(path)
        return True
    except Exception:
        return False


def copy_dir(src: Path, dst: Path) -> bool:
    """Скопировать директорию"""
    try:
        shutil.copytree(src, dst)
        return True
    except Exception:
        return False


def move_dir(src: Path, dst: Path) -> bool:
    """Переместить директорию"""
    try:
        shutil.move(str(src), str(dst))
        return True
    except Exception:
        return False
