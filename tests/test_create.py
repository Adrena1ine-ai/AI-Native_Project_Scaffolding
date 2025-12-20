"""
Тесты команды create
"""

import pytest
from pathlib import Path

from src.commands.create import create_project
from src.core.config import set_default_ide


class TestCreateProject:
    """Тесты создания проекта"""

    def test_create_bot_project(self, temp_dir):
        """Создание проекта с шаблоном bot"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_bot",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_bot"
        assert project_dir.exists()
        
        # Проверяем структуру
        assert (project_dir / "bot").is_dir()
        assert (project_dir / "bot" / "main.py").exists()
        assert (project_dir / "bot" / "handlers").is_dir()
        assert (project_dir / "database").is_dir()
        assert (project_dir / "scripts").is_dir()

    def test_create_webapp_project(self, temp_dir):
        """Создание проекта с шаблоном webapp"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_webapp",
            path=temp_dir,
            template="webapp",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_webapp"
        assert (project_dir / "webapp").is_dir()
        assert (project_dir / "webapp" / "index.html").exists()

    def test_create_fastapi_project(self, temp_dir):
        """Создание проекта с шаблоном fastapi"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_api",
            path=temp_dir,
            template="fastapi",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_api"
        assert (project_dir / "api").is_dir()
        assert (project_dir / "api" / "main.py").exists()
        
        # Проверяем что FastAPI код
        content = (project_dir / "api" / "main.py").read_text()
        assert "FastAPI" in content

    def test_create_full_project(self, temp_dir):
        """Создание проекта с шаблоном full"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_full",
            path=temp_dir,
            template="full",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_full"
        
        # Проверяем все модули
        assert (project_dir / "bot").is_dir()
        assert (project_dir / "webapp").is_dir()
        assert (project_dir / "api").is_dir()
        assert (project_dir / "parser").is_dir()
        assert (project_dir / "database").is_dir()

    def test_create_with_docker(self, temp_dir):
        """Создание проекта с Docker"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_docker",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=True,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_docker"
        assert (project_dir / "Dockerfile").exists()
        assert (project_dir / "docker-compose.yml").exists()
        assert (project_dir / ".dockerignore").exists()

    def test_create_with_ci(self, temp_dir):
        """Создание проекта с CI/CD"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_ci",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=True,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_ci"
        assert (project_dir / ".github" / "workflows" / "ci.yml").exists()
        assert (project_dir / ".github" / "workflows" / "cd.yml").exists()
        assert (project_dir / ".pre-commit-config.yaml").exists()

    def test_create_existing_folder_fails(self, temp_dir):
        """Создание в существующей папке должно падать"""
        set_default_ide("all", ["cursor"])
        
        # Создаём папку
        (temp_dir / "existing").mkdir()
        
        result = create_project(
            name="existing",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
        )
        
        assert result is False

    def test_ai_configs_cursor(self, temp_dir):
        """Проверка создания конфигов для Cursor"""
        set_default_ide("cursor", ["cursor"])
        
        create_project(
            name="test_cursor",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_cursor"
        assert (project_dir / ".cursorrules").exists()
        assert (project_dir / ".cursorignore").exists()
        assert (project_dir / "_AI_INCLUDE").is_dir()

    def test_ai_configs_copilot(self, temp_dir):
        """Проверка создания конфигов для Copilot"""
        set_default_ide("vscode_copilot", ["copilot"])
        
        create_project(
            name="test_copilot",
            path=temp_dir,
            template="bot",
            ai_targets=["copilot"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_copilot"
        assert (project_dir / ".github" / "copilot-instructions.md").exists()

    def test_ai_configs_claude(self, temp_dir):
        """Проверка создания конфигов для Claude"""
        set_default_ide("vscode_claude", ["claude"])
        
        create_project(
            name="test_claude",
            path=temp_dir,
            template="bot",
            ai_targets=["claude"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_claude"
        assert (project_dir / "CLAUDE.md").exists()

    def test_ai_configs_all(self, temp_dir):
        """Проверка создания всех AI конфигов"""
        set_default_ide("all", ["cursor", "copilot", "claude", "windsurf"])
        
        create_project(
            name="test_all",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor", "copilot", "claude", "windsurf"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_all"
        assert (project_dir / ".cursorrules").exists()
        assert (project_dir / ".cursorignore").exists()
        assert (project_dir / ".github" / "copilot-instructions.md").exists()
        assert (project_dir / "CLAUDE.md").exists()
        assert (project_dir / ".windsurfrules").exists()

    def test_scripts_created(self, temp_dir):
        """Проверка создания скриптов"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_scripts",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_scripts"
        scripts_dir = project_dir / "scripts"
        
        assert (scripts_dir / "bootstrap.sh").exists()
        assert (scripts_dir / "bootstrap.ps1").exists()
        assert (scripts_dir / "health_check.sh").exists()
        assert (scripts_dir / "context.py").exists()
        assert (scripts_dir / "check_repo_clean.sh").exists()

    def test_requirements_created(self, temp_dir):
        """Проверка создания requirements.txt"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_req",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_req"
        assert (project_dir / "requirements.txt").exists()
        
        content = (project_dir / "requirements.txt").read_text()
        assert "aiogram" in content


Тесты команды create
"""

import pytest
from pathlib import Path

from src.commands.create import create_project
from src.core.config import set_default_ide


class TestCreateProject:
    """Тесты создания проекта"""

    def test_create_bot_project(self, temp_dir):
        """Создание проекта с шаблоном bot"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_bot",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_bot"
        assert project_dir.exists()
        
        # Проверяем структуру
        assert (project_dir / "bot").is_dir()
        assert (project_dir / "bot" / "main.py").exists()
        assert (project_dir / "bot" / "handlers").is_dir()
        assert (project_dir / "database").is_dir()
        assert (project_dir / "scripts").is_dir()

    def test_create_webapp_project(self, temp_dir):
        """Создание проекта с шаблоном webapp"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_webapp",
            path=temp_dir,
            template="webapp",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_webapp"
        assert (project_dir / "webapp").is_dir()
        assert (project_dir / "webapp" / "index.html").exists()

    def test_create_fastapi_project(self, temp_dir):
        """Создание проекта с шаблоном fastapi"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_api",
            path=temp_dir,
            template="fastapi",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_api"
        assert (project_dir / "api").is_dir()
        assert (project_dir / "api" / "main.py").exists()
        
        # Проверяем что FastAPI код
        content = (project_dir / "api" / "main.py").read_text()
        assert "FastAPI" in content

    def test_create_full_project(self, temp_dir):
        """Создание проекта с шаблоном full"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_full",
            path=temp_dir,
            template="full",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_full"
        
        # Проверяем все модули
        assert (project_dir / "bot").is_dir()
        assert (project_dir / "webapp").is_dir()
        assert (project_dir / "api").is_dir()
        assert (project_dir / "parser").is_dir()
        assert (project_dir / "database").is_dir()

    def test_create_with_docker(self, temp_dir):
        """Создание проекта с Docker"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_docker",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=True,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_docker"
        assert (project_dir / "Dockerfile").exists()
        assert (project_dir / "docker-compose.yml").exists()
        assert (project_dir / ".dockerignore").exists()

    def test_create_with_ci(self, temp_dir):
        """Создание проекта с CI/CD"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_ci",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=True,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_ci"
        assert (project_dir / ".github" / "workflows" / "ci.yml").exists()
        assert (project_dir / ".github" / "workflows" / "cd.yml").exists()
        assert (project_dir / ".pre-commit-config.yaml").exists()

    def test_create_existing_folder_fails(self, temp_dir):
        """Создание в существующей папке должно падать"""
        set_default_ide("all", ["cursor"])
        
        # Создаём папку
        (temp_dir / "existing").mkdir()
        
        result = create_project(
            name="existing",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
        )
        
        assert result is False

    def test_ai_configs_cursor(self, temp_dir):
        """Проверка создания конфигов для Cursor"""
        set_default_ide("cursor", ["cursor"])
        
        create_project(
            name="test_cursor",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_cursor"
        assert (project_dir / ".cursorrules").exists()
        assert (project_dir / ".cursorignore").exists()
        assert (project_dir / "_AI_INCLUDE").is_dir()

    def test_ai_configs_copilot(self, temp_dir):
        """Проверка создания конфигов для Copilot"""
        set_default_ide("vscode_copilot", ["copilot"])
        
        create_project(
            name="test_copilot",
            path=temp_dir,
            template="bot",
            ai_targets=["copilot"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_copilot"
        assert (project_dir / ".github" / "copilot-instructions.md").exists()

    def test_ai_configs_claude(self, temp_dir):
        """Проверка создания конфигов для Claude"""
        set_default_ide("vscode_claude", ["claude"])
        
        create_project(
            name="test_claude",
            path=temp_dir,
            template="bot",
            ai_targets=["claude"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_claude"
        assert (project_dir / "CLAUDE.md").exists()

    def test_ai_configs_all(self, temp_dir):
        """Проверка создания всех AI конфигов"""
        set_default_ide("all", ["cursor", "copilot", "claude", "windsurf"])
        
        create_project(
            name="test_all",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor", "copilot", "claude", "windsurf"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_all"
        assert (project_dir / ".cursorrules").exists()
        assert (project_dir / ".cursorignore").exists()
        assert (project_dir / ".github" / "copilot-instructions.md").exists()
        assert (project_dir / "CLAUDE.md").exists()
        assert (project_dir / ".windsurfrules").exists()

    def test_scripts_created(self, temp_dir):
        """Проверка создания скриптов"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_scripts",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_scripts"
        scripts_dir = project_dir / "scripts"
        
        assert (scripts_dir / "bootstrap.sh").exists()
        assert (scripts_dir / "bootstrap.ps1").exists()
        assert (scripts_dir / "health_check.sh").exists()
        assert (scripts_dir / "context.py").exists()
        assert (scripts_dir / "check_repo_clean.sh").exists()

    def test_requirements_created(self, temp_dir):
        """Проверка создания requirements.txt"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_req",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_req"
        assert (project_dir / "requirements.txt").exists()
        
        content = (project_dir / "requirements.txt").read_text()
        assert "aiogram" in content


Тесты команды create
"""

import pytest
from pathlib import Path

from src.commands.create import create_project
from src.core.config import set_default_ide


class TestCreateProject:
    """Тесты создания проекта"""

    def test_create_bot_project(self, temp_dir):
        """Создание проекта с шаблоном bot"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_bot",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_bot"
        assert project_dir.exists()
        
        # Проверяем структуру
        assert (project_dir / "bot").is_dir()
        assert (project_dir / "bot" / "main.py").exists()
        assert (project_dir / "bot" / "handlers").is_dir()
        assert (project_dir / "database").is_dir()
        assert (project_dir / "scripts").is_dir()

    def test_create_webapp_project(self, temp_dir):
        """Создание проекта с шаблоном webapp"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_webapp",
            path=temp_dir,
            template="webapp",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_webapp"
        assert (project_dir / "webapp").is_dir()
        assert (project_dir / "webapp" / "index.html").exists()

    def test_create_fastapi_project(self, temp_dir):
        """Создание проекта с шаблоном fastapi"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_api",
            path=temp_dir,
            template="fastapi",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_api"
        assert (project_dir / "api").is_dir()
        assert (project_dir / "api" / "main.py").exists()
        
        # Проверяем что FastAPI код
        content = (project_dir / "api" / "main.py").read_text()
        assert "FastAPI" in content

    def test_create_full_project(self, temp_dir):
        """Создание проекта с шаблоном full"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_full",
            path=temp_dir,
            template="full",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_full"
        
        # Проверяем все модули
        assert (project_dir / "bot").is_dir()
        assert (project_dir / "webapp").is_dir()
        assert (project_dir / "api").is_dir()
        assert (project_dir / "parser").is_dir()
        assert (project_dir / "database").is_dir()

    def test_create_with_docker(self, temp_dir):
        """Создание проекта с Docker"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_docker",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=True,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_docker"
        assert (project_dir / "Dockerfile").exists()
        assert (project_dir / "docker-compose.yml").exists()
        assert (project_dir / ".dockerignore").exists()

    def test_create_with_ci(self, temp_dir):
        """Создание проекта с CI/CD"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_ci",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=True,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_ci"
        assert (project_dir / ".github" / "workflows" / "ci.yml").exists()
        assert (project_dir / ".github" / "workflows" / "cd.yml").exists()
        assert (project_dir / ".pre-commit-config.yaml").exists()

    def test_create_existing_folder_fails(self, temp_dir):
        """Создание в существующей папке должно падать"""
        set_default_ide("all", ["cursor"])
        
        # Создаём папку
        (temp_dir / "existing").mkdir()
        
        result = create_project(
            name="existing",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
        )
        
        assert result is False

    def test_ai_configs_cursor(self, temp_dir):
        """Проверка создания конфигов для Cursor"""
        set_default_ide("cursor", ["cursor"])
        
        create_project(
            name="test_cursor",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_cursor"
        assert (project_dir / ".cursorrules").exists()
        assert (project_dir / ".cursorignore").exists()
        assert (project_dir / "_AI_INCLUDE").is_dir()

    def test_ai_configs_copilot(self, temp_dir):
        """Проверка создания конфигов для Copilot"""
        set_default_ide("vscode_copilot", ["copilot"])
        
        create_project(
            name="test_copilot",
            path=temp_dir,
            template="bot",
            ai_targets=["copilot"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_copilot"
        assert (project_dir / ".github" / "copilot-instructions.md").exists()

    def test_ai_configs_claude(self, temp_dir):
        """Проверка создания конфигов для Claude"""
        set_default_ide("vscode_claude", ["claude"])
        
        create_project(
            name="test_claude",
            path=temp_dir,
            template="bot",
            ai_targets=["claude"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_claude"
        assert (project_dir / "CLAUDE.md").exists()

    def test_ai_configs_all(self, temp_dir):
        """Проверка создания всех AI конфигов"""
        set_default_ide("all", ["cursor", "copilot", "claude", "windsurf"])
        
        create_project(
            name="test_all",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor", "copilot", "claude", "windsurf"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_all"
        assert (project_dir / ".cursorrules").exists()
        assert (project_dir / ".cursorignore").exists()
        assert (project_dir / ".github" / "copilot-instructions.md").exists()
        assert (project_dir / "CLAUDE.md").exists()
        assert (project_dir / ".windsurfrules").exists()

    def test_scripts_created(self, temp_dir):
        """Проверка создания скриптов"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_scripts",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_scripts"
        scripts_dir = project_dir / "scripts"
        
        assert (scripts_dir / "bootstrap.sh").exists()
        assert (scripts_dir / "bootstrap.ps1").exists()
        assert (scripts_dir / "health_check.sh").exists()
        assert (scripts_dir / "context.py").exists()
        assert (scripts_dir / "check_repo_clean.sh").exists()

    def test_requirements_created(self, temp_dir):
        """Проверка создания requirements.txt"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_req",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_req"
        assert (project_dir / "requirements.txt").exists()
        
        content = (project_dir / "requirements.txt").read_text()
        assert "aiogram" in content


Тесты команды create
"""

import pytest
from pathlib import Path

from src.commands.create import create_project
from src.core.config import set_default_ide


class TestCreateProject:
    """Тесты создания проекта"""

    def test_create_bot_project(self, temp_dir):
        """Создание проекта с шаблоном bot"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_bot",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_bot"
        assert project_dir.exists()
        
        # Проверяем структуру
        assert (project_dir / "bot").is_dir()
        assert (project_dir / "bot" / "main.py").exists()
        assert (project_dir / "bot" / "handlers").is_dir()
        assert (project_dir / "database").is_dir()
        assert (project_dir / "scripts").is_dir()

    def test_create_webapp_project(self, temp_dir):
        """Создание проекта с шаблоном webapp"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_webapp",
            path=temp_dir,
            template="webapp",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_webapp"
        assert (project_dir / "webapp").is_dir()
        assert (project_dir / "webapp" / "index.html").exists()

    def test_create_fastapi_project(self, temp_dir):
        """Создание проекта с шаблоном fastapi"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_api",
            path=temp_dir,
            template="fastapi",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_api"
        assert (project_dir / "api").is_dir()
        assert (project_dir / "api" / "main.py").exists()
        
        # Проверяем что FastAPI код
        content = (project_dir / "api" / "main.py").read_text()
        assert "FastAPI" in content

    def test_create_full_project(self, temp_dir):
        """Создание проекта с шаблоном full"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_full",
            path=temp_dir,
            template="full",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_full"
        
        # Проверяем все модули
        assert (project_dir / "bot").is_dir()
        assert (project_dir / "webapp").is_dir()
        assert (project_dir / "api").is_dir()
        assert (project_dir / "parser").is_dir()
        assert (project_dir / "database").is_dir()

    def test_create_with_docker(self, temp_dir):
        """Создание проекта с Docker"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_docker",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=True,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_docker"
        assert (project_dir / "Dockerfile").exists()
        assert (project_dir / "docker-compose.yml").exists()
        assert (project_dir / ".dockerignore").exists()

    def test_create_with_ci(self, temp_dir):
        """Создание проекта с CI/CD"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_ci",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=True,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_ci"
        assert (project_dir / ".github" / "workflows" / "ci.yml").exists()
        assert (project_dir / ".github" / "workflows" / "cd.yml").exists()
        assert (project_dir / ".pre-commit-config.yaml").exists()

    def test_create_existing_folder_fails(self, temp_dir):
        """Создание в существующей папке должно падать"""
        set_default_ide("all", ["cursor"])
        
        # Создаём папку
        (temp_dir / "existing").mkdir()
        
        result = create_project(
            name="existing",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
        )
        
        assert result is False

    def test_ai_configs_cursor(self, temp_dir):
        """Проверка создания конфигов для Cursor"""
        set_default_ide("cursor", ["cursor"])
        
        create_project(
            name="test_cursor",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_cursor"
        assert (project_dir / ".cursorrules").exists()
        assert (project_dir / ".cursorignore").exists()
        assert (project_dir / "_AI_INCLUDE").is_dir()

    def test_ai_configs_copilot(self, temp_dir):
        """Проверка создания конфигов для Copilot"""
        set_default_ide("vscode_copilot", ["copilot"])
        
        create_project(
            name="test_copilot",
            path=temp_dir,
            template="bot",
            ai_targets=["copilot"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_copilot"
        assert (project_dir / ".github" / "copilot-instructions.md").exists()

    def test_ai_configs_claude(self, temp_dir):
        """Проверка создания конфигов для Claude"""
        set_default_ide("vscode_claude", ["claude"])
        
        create_project(
            name="test_claude",
            path=temp_dir,
            template="bot",
            ai_targets=["claude"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_claude"
        assert (project_dir / "CLAUDE.md").exists()

    def test_ai_configs_all(self, temp_dir):
        """Проверка создания всех AI конфигов"""
        set_default_ide("all", ["cursor", "copilot", "claude", "windsurf"])
        
        create_project(
            name="test_all",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor", "copilot", "claude", "windsurf"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_all"
        assert (project_dir / ".cursorrules").exists()
        assert (project_dir / ".cursorignore").exists()
        assert (project_dir / ".github" / "copilot-instructions.md").exists()
        assert (project_dir / "CLAUDE.md").exists()
        assert (project_dir / ".windsurfrules").exists()

    def test_scripts_created(self, temp_dir):
        """Проверка создания скриптов"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_scripts",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_scripts"
        scripts_dir = project_dir / "scripts"
        
        assert (scripts_dir / "bootstrap.sh").exists()
        assert (scripts_dir / "bootstrap.ps1").exists()
        assert (scripts_dir / "health_check.sh").exists()
        assert (scripts_dir / "context.py").exists()
        assert (scripts_dir / "check_repo_clean.sh").exists()

    def test_requirements_created(self, temp_dir):
        """Проверка создания requirements.txt"""
        set_default_ide("all", ["cursor"])
        
        create_project(
            name="test_req",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test_req"
        assert (project_dir / "requirements.txt").exists()
        
        content = (project_dir / "requirements.txt").read_text()
        assert "aiogram" in content

