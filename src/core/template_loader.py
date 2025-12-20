"""
Загрузчик шаблонов из файлов
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .file_utils import create_file
from .constants import COLORS


# Путь к папке templates
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


def load_template(template_path: str) -> str | None:
    """
    Загрузить шаблон из файла
    
    Args:
        template_path: Относительный путь к шаблону (например, "bot/main.py.template")
        
    Returns:
        Содержимое шаблона или None если не найден
    """
    full_path = TEMPLATES_DIR / template_path
    
    if full_path.exists():
        return full_path.read_text(encoding="utf-8")
    
    return None


def render_template(content: str, context: dict[str, Any]) -> str:
    """
    Рендеринг шаблона с подстановкой переменных
    
    Поддерживает синтаксис:
        {{variable}} — обязательная переменная
        {{variable|default}} — с дефолтным значением
    
    Args:
        content: Содержимое шаблона
        context: Словарь переменных
        
    Returns:
        Отрендеренный шаблон
    """
    import re
    
    # Паттерн для {{variable}} или {{variable|default}}
    pattern = r'\{\{(\w+)(?:\|([^}]*))?\}\}'
    
    def replacer(match: re.Match) -> str:
        var_name = match.group(1)
        default = match.group(2)
        
        if var_name in context:
            return str(context[var_name])
        elif default is not None:
            return default
        else:
            return match.group(0)  # Оставить как есть
    
    return re.sub(pattern, replacer, content)


def copy_template_file(
    template_name: str,
    dest_path: Path,
    context: dict[str, Any],
    executable: bool = False
) -> bool:
    """
    Скопировать файл шаблона с рендерингом
    
    Args:
        template_name: Имя шаблона (например, "bot/main.py.template")
        dest_path: Путь назначения
        context: Контекст для рендеринга
        executable: Сделать файл исполняемым
        
    Returns:
        True если успешно
    """
    content = load_template(template_name)
    
    if content is None:
        return False
    
    rendered = render_template(content, context)
    create_file(dest_path, rendered, executable=executable)
    
    return True


def list_templates() -> dict[str, list[str]]:
    """
    Получить список всех доступных шаблонов
    
    Returns:
        Словарь {категория: [файлы]}
    """
    templates: dict[str, list[str]] = {}
    
    if not TEMPLATES_DIR.exists():
        return templates
    
    for category_dir in TEMPLATES_DIR.iterdir():
        if category_dir.is_dir():
            files = []
            for template_file in category_dir.rglob("*.template"):
                rel_path = template_file.relative_to(TEMPLATES_DIR)
                files.append(str(rel_path))
            
            if files:
                templates[category_dir.name] = sorted(files)
    
    return templates


def get_template_info(template_name: str) -> dict[str, Any] | None:
    """
    Получить информацию о шаблоне
    
    Args:
        template_name: Имя категории шаблона (bot, webapp, etc.)
        
    Returns:
        Словарь с информацией или None
    """
    template_dir = TEMPLATES_DIR / template_name
    
    if not template_dir.is_dir():
        return None
    
    # Ищем README или описание
    readme = template_dir / "README.md"
    description = ""
    
    if readme.exists():
        description = readme.read_text(encoding="utf-8")
    
    files = list(template_dir.rglob("*.template"))
    
    return {
        "name": template_name,
        "path": str(template_dir),
        "description": description,
        "files_count": len(files),
        "files": [str(f.relative_to(template_dir)) for f in files],
    }


Загрузчик шаблонов из файлов
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .file_utils import create_file
from .constants import COLORS


# Путь к папке templates
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


def load_template(template_path: str) -> str | None:
    """
    Загрузить шаблон из файла
    
    Args:
        template_path: Относительный путь к шаблону (например, "bot/main.py.template")
        
    Returns:
        Содержимое шаблона или None если не найден
    """
    full_path = TEMPLATES_DIR / template_path
    
    if full_path.exists():
        return full_path.read_text(encoding="utf-8")
    
    return None


def render_template(content: str, context: dict[str, Any]) -> str:
    """
    Рендеринг шаблона с подстановкой переменных
    
    Поддерживает синтаксис:
        {{variable}} — обязательная переменная
        {{variable|default}} — с дефолтным значением
    
    Args:
        content: Содержимое шаблона
        context: Словарь переменных
        
    Returns:
        Отрендеренный шаблон
    """
    import re
    
    # Паттерн для {{variable}} или {{variable|default}}
    pattern = r'\{\{(\w+)(?:\|([^}]*))?\}\}'
    
    def replacer(match: re.Match) -> str:
        var_name = match.group(1)
        default = match.group(2)
        
        if var_name in context:
            return str(context[var_name])
        elif default is not None:
            return default
        else:
            return match.group(0)  # Оставить как есть
    
    return re.sub(pattern, replacer, content)


def copy_template_file(
    template_name: str,
    dest_path: Path,
    context: dict[str, Any],
    executable: bool = False
) -> bool:
    """
    Скопировать файл шаблона с рендерингом
    
    Args:
        template_name: Имя шаблона (например, "bot/main.py.template")
        dest_path: Путь назначения
        context: Контекст для рендеринга
        executable: Сделать файл исполняемым
        
    Returns:
        True если успешно
    """
    content = load_template(template_name)
    
    if content is None:
        return False
    
    rendered = render_template(content, context)
    create_file(dest_path, rendered, executable=executable)
    
    return True


def list_templates() -> dict[str, list[str]]:
    """
    Получить список всех доступных шаблонов
    
    Returns:
        Словарь {категория: [файлы]}
    """
    templates: dict[str, list[str]] = {}
    
    if not TEMPLATES_DIR.exists():
        return templates
    
    for category_dir in TEMPLATES_DIR.iterdir():
        if category_dir.is_dir():
            files = []
            for template_file in category_dir.rglob("*.template"):
                rel_path = template_file.relative_to(TEMPLATES_DIR)
                files.append(str(rel_path))
            
            if files:
                templates[category_dir.name] = sorted(files)
    
    return templates


def get_template_info(template_name: str) -> dict[str, Any] | None:
    """
    Получить информацию о шаблоне
    
    Args:
        template_name: Имя категории шаблона (bot, webapp, etc.)
        
    Returns:
        Словарь с информацией или None
    """
    template_dir = TEMPLATES_DIR / template_name
    
    if not template_dir.is_dir():
        return None
    
    # Ищем README или описание
    readme = template_dir / "README.md"
    description = ""
    
    if readme.exists():
        description = readme.read_text(encoding="utf-8")
    
    files = list(template_dir.rglob("*.template"))
    
    return {
        "name": template_name,
        "path": str(template_dir),
        "description": description,
        "files_count": len(files),
        "files": [str(f.relative_to(template_dir)) for f in files],
    }


Загрузчик шаблонов из файлов
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .file_utils import create_file
from .constants import COLORS


# Путь к папке templates
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


def load_template(template_path: str) -> str | None:
    """
    Загрузить шаблон из файла
    
    Args:
        template_path: Относительный путь к шаблону (например, "bot/main.py.template")
        
    Returns:
        Содержимое шаблона или None если не найден
    """
    full_path = TEMPLATES_DIR / template_path
    
    if full_path.exists():
        return full_path.read_text(encoding="utf-8")
    
    return None


def render_template(content: str, context: dict[str, Any]) -> str:
    """
    Рендеринг шаблона с подстановкой переменных
    
    Поддерживает синтаксис:
        {{variable}} — обязательная переменная
        {{variable|default}} — с дефолтным значением
    
    Args:
        content: Содержимое шаблона
        context: Словарь переменных
        
    Returns:
        Отрендеренный шаблон
    """
    import re
    
    # Паттерн для {{variable}} или {{variable|default}}
    pattern = r'\{\{(\w+)(?:\|([^}]*))?\}\}'
    
    def replacer(match: re.Match) -> str:
        var_name = match.group(1)
        default = match.group(2)
        
        if var_name in context:
            return str(context[var_name])
        elif default is not None:
            return default
        else:
            return match.group(0)  # Оставить как есть
    
    return re.sub(pattern, replacer, content)


def copy_template_file(
    template_name: str,
    dest_path: Path,
    context: dict[str, Any],
    executable: bool = False
) -> bool:
    """
    Скопировать файл шаблона с рендерингом
    
    Args:
        template_name: Имя шаблона (например, "bot/main.py.template")
        dest_path: Путь назначения
        context: Контекст для рендеринга
        executable: Сделать файл исполняемым
        
    Returns:
        True если успешно
    """
    content = load_template(template_name)
    
    if content is None:
        return False
    
    rendered = render_template(content, context)
    create_file(dest_path, rendered, executable=executable)
    
    return True


def list_templates() -> dict[str, list[str]]:
    """
    Получить список всех доступных шаблонов
    
    Returns:
        Словарь {категория: [файлы]}
    """
    templates: dict[str, list[str]] = {}
    
    if not TEMPLATES_DIR.exists():
        return templates
    
    for category_dir in TEMPLATES_DIR.iterdir():
        if category_dir.is_dir():
            files = []
            for template_file in category_dir.rglob("*.template"):
                rel_path = template_file.relative_to(TEMPLATES_DIR)
                files.append(str(rel_path))
            
            if files:
                templates[category_dir.name] = sorted(files)
    
    return templates


def get_template_info(template_name: str) -> dict[str, Any] | None:
    """
    Получить информацию о шаблоне
    
    Args:
        template_name: Имя категории шаблона (bot, webapp, etc.)
        
    Returns:
        Словарь с информацией или None
    """
    template_dir = TEMPLATES_DIR / template_name
    
    if not template_dir.is_dir():
        return None
    
    # Ищем README или описание
    readme = template_dir / "README.md"
    description = ""
    
    if readme.exists():
        description = readme.read_text(encoding="utf-8")
    
    files = list(template_dir.rglob("*.template"))
    
    return {
        "name": template_name,
        "path": str(template_dir),
        "description": description,
        "files_count": len(files),
        "files": [str(f.relative_to(template_dir)) for f in files],
    }


Загрузчик шаблонов из файлов
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .file_utils import create_file
from .constants import COLORS


# Путь к папке templates
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


def load_template(template_path: str) -> str | None:
    """
    Загрузить шаблон из файла
    
    Args:
        template_path: Относительный путь к шаблону (например, "bot/main.py.template")
        
    Returns:
        Содержимое шаблона или None если не найден
    """
    full_path = TEMPLATES_DIR / template_path
    
    if full_path.exists():
        return full_path.read_text(encoding="utf-8")
    
    return None


def render_template(content: str, context: dict[str, Any]) -> str:
    """
    Рендеринг шаблона с подстановкой переменных
    
    Поддерживает синтаксис:
        {{variable}} — обязательная переменная
        {{variable|default}} — с дефолтным значением
    
    Args:
        content: Содержимое шаблона
        context: Словарь переменных
        
    Returns:
        Отрендеренный шаблон
    """
    import re
    
    # Паттерн для {{variable}} или {{variable|default}}
    pattern = r'\{\{(\w+)(?:\|([^}]*))?\}\}'
    
    def replacer(match: re.Match) -> str:
        var_name = match.group(1)
        default = match.group(2)
        
        if var_name in context:
            return str(context[var_name])
        elif default is not None:
            return default
        else:
            return match.group(0)  # Оставить как есть
    
    return re.sub(pattern, replacer, content)


def copy_template_file(
    template_name: str,
    dest_path: Path,
    context: dict[str, Any],
    executable: bool = False
) -> bool:
    """
    Скопировать файл шаблона с рендерингом
    
    Args:
        template_name: Имя шаблона (например, "bot/main.py.template")
        dest_path: Путь назначения
        context: Контекст для рендеринга
        executable: Сделать файл исполняемым
        
    Returns:
        True если успешно
    """
    content = load_template(template_name)
    
    if content is None:
        return False
    
    rendered = render_template(content, context)
    create_file(dest_path, rendered, executable=executable)
    
    return True


def list_templates() -> dict[str, list[str]]:
    """
    Получить список всех доступных шаблонов
    
    Returns:
        Словарь {категория: [файлы]}
    """
    templates: dict[str, list[str]] = {}
    
    if not TEMPLATES_DIR.exists():
        return templates
    
    for category_dir in TEMPLATES_DIR.iterdir():
        if category_dir.is_dir():
            files = []
            for template_file in category_dir.rglob("*.template"):
                rel_path = template_file.relative_to(TEMPLATES_DIR)
                files.append(str(rel_path))
            
            if files:
                templates[category_dir.name] = sorted(files)
    
    return templates


def get_template_info(template_name: str) -> dict[str, Any] | None:
    """
    Получить информацию о шаблоне
    
    Args:
        template_name: Имя категории шаблона (bot, webapp, etc.)
        
    Returns:
        Словарь с информацией или None
    """
    template_dir = TEMPLATES_DIR / template_name
    
    if not template_dir.is_dir():
        return None
    
    # Ищем README или описание
    readme = template_dir / "README.md"
    description = ""
    
    if readme.exists():
        description = readme.read_text(encoding="utf-8")
    
    files = list(template_dir.rglob("*.template"))
    
    return {
        "name": template_name,
        "path": str(template_dir),
        "description": description,
        "files_count": len(files),
        "files": [str(f.relative_to(template_dir)) for f in files],
    }

