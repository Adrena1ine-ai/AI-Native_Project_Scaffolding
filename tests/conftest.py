"""
Pytest fixtures для AI Toolkit
"""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Временная директория для тестов"""
    tmp = tempfile.mkdtemp(prefix="ai_toolkit_test_")
    yield Path(tmp)
    # Cleanup
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def temp_project(temp_dir):
    """Создаёт временную папку проекта"""
    project_dir = temp_dir / "test_project"
    project_dir.mkdir()
    return project_dir


@pytest.fixture
def temp_project_with_venv(temp_project):
    """Проект с venv внутри (для тестов cleanup)"""
    venv_dir = temp_project / "venv"
    venv_dir.mkdir()
    (venv_dir / "bin").mkdir()
    (venv_dir / "bin" / "python").touch()
    (venv_dir / "lib").mkdir()
    return temp_project


@pytest.fixture
def temp_project_with_files(temp_project):
    """Проект с базовыми файлами"""
    # Создаём структуру
    (temp_project / "bot").mkdir()
    (temp_project / "bot" / "__init__.py").touch()
    (temp_project / "requirements.txt").write_text("aiogram>=3.4\n")
    (temp_project / ".env.example").write_text("BOT_TOKEN=xxx\n")
    return temp_project


@pytest.fixture
def clean_project(temp_dir):
    """Чистый проект с правильной структурой"""
    from src.commands.create import create_project
    from src.core.config import set_default_ide
    
    set_default_ide("all", ["cursor", "copilot", "claude"])
    
    project_dir = temp_dir / "clean_project"
    create_project(
        name="clean_project",
        path=temp_dir,
        template="bot",
        ai_targets=["cursor", "copilot"],
        include_docker=False,
        include_ci=False,
        include_git=False,
    )
    
    return project_dir

