"""
Tests for create command
"""

import pytest
from pathlib import Path

from src.commands.create import create_project
from src.core.config import set_default_ide


class TestCreateProject:
    """Tests for project creation"""

    def test_create_bot_project(self, temp_dir):
        """Create project with bot template"""
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
        
        # Check structure
        assert (project_dir / "bot").is_dir()
        assert (project_dir / "bot" / "main.py").exists()
        assert (project_dir / "bot" / "handlers").is_dir()
        assert (project_dir / "database").is_dir()
        assert (project_dir / "scripts").is_dir()

    def test_create_webapp_project(self, temp_dir):
        """Create project with webapp template"""
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
        """Create project with fastapi template"""
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
        
        # Check FastAPI code
        content = (project_dir / "api" / "main.py").read_text()
        assert "FastAPI" in content

    def test_create_full_project(self, temp_dir):
        """Create project with full template"""
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
        
        # Check all modules
        assert (project_dir / "bot").is_dir()
        assert (project_dir / "webapp").is_dir()
        assert (project_dir / "api").is_dir()
        assert (project_dir / "parser").is_dir()

    def test_create_with_docker(self, temp_dir):
        """Create project with Docker"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_docker",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=True,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_docker"
        assert (project_dir / "Dockerfile").exists()
        assert (project_dir / "docker-compose.yml").exists()
        assert (project_dir / ".dockerignore").exists()

    def test_create_with_ci(self, temp_dir):
        """Create project with CI/CD"""
        set_default_ide("all", ["cursor"])
        
        result = create_project(
            name="test_ci",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=True,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_ci"
        workflows = project_dir / ".github" / "workflows"
        assert workflows.is_dir()
        assert (workflows / "ci.yml").exists()

    def test_create_with_multiple_ides(self, temp_dir):
        """Create project with multiple IDE configs"""
        set_default_ide("all", ["cursor", "copilot", "claude"])
        
        result = create_project(
            name="test_multi",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor", "copilot", "claude"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is True
        project_dir = temp_dir / "test_multi"
        assert (project_dir / ".cursorrules").exists()
        assert (project_dir / ".github" / "copilot-instructions.md").exists()
        assert (project_dir / "CLAUDE.md").exists()

    def test_create_fails_if_exists(self, temp_dir):
        """Create fails if project exists"""
        (temp_dir / "existing").mkdir()
        
        result = create_project(
            name="existing",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is False

    def test_create_with_invalid_name(self, temp_dir):
        """Create fails with invalid name"""
        result = create_project(
            name="invalid name!",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        assert result is False


class TestProjectStructure:
    """Tests for created project structure"""

    def test_ai_include_created(self, temp_dir):
        """_AI_INCLUDE created"""
        create_project(
            name="test",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        ai_dir = temp_dir / "test" / "_AI_INCLUDE"
        assert ai_dir.is_dir()
        assert (ai_dir / "PROJECT_CONVENTIONS.md").exists()
        assert (ai_dir / "WHERE_IS_WHAT.md").exists()

    def test_scripts_created(self, temp_dir):
        """Scripts created"""
        create_project(
            name="test",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        scripts = temp_dir / "test" / "scripts"
        assert scripts.is_dir()
        assert (scripts / "bootstrap.sh").exists()
        assert (scripts / "context.py").exists()

    def test_requirements_created(self, temp_dir):
        """Requirements created"""
        create_project(
            name="test",
            path=temp_dir,
            template="bot",
            ai_targets=["cursor"],
            include_docker=False,
            include_ci=False,
            include_git=False,
        )
        
        project_dir = temp_dir / "test"
        assert (project_dir / "requirements.txt").exists()
        assert (project_dir / "requirements-dev.txt").exists()
