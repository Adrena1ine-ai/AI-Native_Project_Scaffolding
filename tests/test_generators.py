"""
Tests for generators
"""

import pytest
from pathlib import Path

from src.generators.ai_configs import (
    generate_cursor_rules,
    generate_cursor_ignore,
    generate_copilot_instructions,
    generate_claude_md,
    generate_windsurf_rules,
    generate_ai_include,
    get_common_rules,
)
from src.generators.scripts import (
    generate_bootstrap_sh,
    generate_bootstrap_ps1,
    generate_context_switcher,
    generate_health_check,
    generate_check_repo_clean,
)
from src.generators.docker import (
    generate_dockerfile,
    generate_docker_compose,
    generate_dockerignore,
)
from src.generators.ci_cd import (
    generate_ci_workflow,
    generate_cd_workflow,
    generate_pre_commit_config,
    generate_dependabot,
)
from src.generators.project_files import (
    generate_requirements,
    generate_config_py,
    generate_env_example,
    generate_readme,
    generate_gitignore,
)


class TestAIConfigs:
    """Tests for AI config generation"""

    def test_common_rules_contains_project_name(self):
        """Common rules contain project name"""
        result = get_common_rules("my_project", "2024-01-01")
        assert "my_project" in result

    def test_cursor_rules_created(self, temp_project):
        """Create .cursorrules"""
        generate_cursor_rules(temp_project, "test", "2024-01-01")
        
        assert (temp_project / ".cursorrules").exists()
        content = (temp_project / ".cursorrules").read_text()
        assert "test" in content

    def test_cursor_ignore_created(self, temp_project):
        """Create .cursorignore"""
        generate_cursor_ignore(temp_project, "test", "2024-01-01")
        
        assert (temp_project / ".cursorignore").exists()
        content = (temp_project / ".cursorignore").read_text()
        assert "venv/" in content
        assert "__pycache__" in content

    def test_copilot_instructions_created(self, temp_project):
        """Create copilot-instructions.md"""
        generate_copilot_instructions(temp_project, "test", "2024-01-01")
        
        path = temp_project / ".github" / "copilot-instructions.md"
        assert path.exists()
        content = path.read_text()
        assert "Copilot" in content

    def test_claude_md_created(self, temp_project):
        """Create CLAUDE.md"""
        generate_claude_md(temp_project, "test", "2024-01-01")
        
        assert (temp_project / "CLAUDE.md").exists()
        content = (temp_project / "CLAUDE.md").read_text()
        assert "Claude" in content

    def test_windsurf_rules_created(self, temp_project):
        """Create .windsurfrules"""
        generate_windsurf_rules(temp_project, "test", "2024-01-01")
        
        assert (temp_project / ".windsurfrules").exists()

    def test_ai_include_created(self, temp_project):
        """Create _AI_INCLUDE/"""
        generate_ai_include(temp_project, "test", "2024-01-01")
        
        ai_dir = temp_project / "_AI_INCLUDE"
        assert ai_dir.is_dir()
        assert (ai_dir / "PROJECT_CONVENTIONS.md").exists()
        assert (ai_dir / "WHERE_IS_WHAT.md").exists()


class TestScripts:
    """Tests for script generation"""

    def test_bootstrap_sh_created(self, temp_project):
        """Create bootstrap.sh"""
        generate_bootstrap_sh(temp_project, "test")
        
        path = temp_project / "scripts" / "bootstrap.sh"
        assert path.exists()
        
        content = path.read_text()
        assert "_venvs" in content
        assert "test" in content

    def test_bootstrap_ps1_created(self, temp_project):
        """Create bootstrap.ps1"""
        generate_bootstrap_ps1(temp_project, "test")
        
        path = temp_project / "scripts" / "bootstrap.ps1"
        assert path.exists()
        
        content = path.read_text()
        assert "_venvs" in content

    def test_context_switcher_created(self, temp_project):
        """Create context.py"""
        generate_context_switcher(temp_project)
        
        path = temp_project / "scripts" / "context.py"
        assert path.exists()
        
        content = path.read_text()
        assert "MODULES" in content


class TestDocker:
    """Tests for Docker generation"""

    def test_dockerfile_created(self, temp_project):
        """Create Dockerfile"""
        generate_dockerfile(temp_project, "test")
        
        assert (temp_project / "Dockerfile").exists()
        content = (temp_project / "Dockerfile").read_text()
        assert "python" in content.lower()

    def test_docker_compose_created(self, temp_project):
        """Create docker-compose.yml"""
        generate_docker_compose(temp_project, "test")
        
        assert (temp_project / "docker-compose.yml").exists()
        content = (temp_project / "docker-compose.yml").read_text()
        assert "test" in content

    def test_dockerignore_created(self, temp_project):
        """Create .dockerignore"""
        generate_dockerignore(temp_project)
        
        assert (temp_project / ".dockerignore").exists()
        content = (temp_project / ".dockerignore").read_text()
        assert "venv" in content
        assert "__pycache__" in content


class TestCICD:
    """Tests for CI/CD generation"""

    def test_ci_workflow_created(self, temp_project):
        """Create ci.yml"""
        generate_ci_workflow(temp_project)
        
        path = temp_project / ".github" / "workflows" / "ci.yml"
        assert path.exists()
        content = path.read_text()
        assert "pytest" in content or "ruff" in content

    def test_cd_workflow_created(self, temp_project):
        """Create cd.yml"""
        generate_cd_workflow(temp_project)
        
        path = temp_project / ".github" / "workflows" / "cd.yml"
        assert path.exists()

    def test_pre_commit_created(self, temp_project):
        """Create .pre-commit-config.yaml"""
        generate_pre_commit_config(temp_project)
        
        assert (temp_project / ".pre-commit-config.yaml").exists()

    def test_dependabot_created(self, temp_project):
        """Create dependabot.yml"""
        generate_dependabot(temp_project)
        
        path = temp_project / ".github" / "dependabot.yml"
        assert path.exists()


class TestProjectFiles:
    """Tests for project file generation"""

    def test_requirements_created(self, temp_project):
        """Create requirements.txt"""
        generate_requirements(temp_project, "bot")
        
        assert (temp_project / "requirements.txt").exists()
        content = (temp_project / "requirements.txt").read_text()
        assert len(content) > 0

    def test_config_py_created(self, temp_project):
        """Create config.py"""
        generate_config_py(temp_project, "bot")
        
        assert (temp_project / "config.py").exists()
        content = (temp_project / "config.py").read_text()
        assert "BaseSettings" in content or "class" in content

    def test_env_example_created(self, temp_project):
        """Create .env.example"""
        generate_env_example(temp_project, "bot")
        
        assert (temp_project / ".env.example").exists()

    def test_readme_created(self, temp_project):
        """Create README.md"""
        generate_readme(temp_project, "test", "bot")
        
        assert (temp_project / "README.md").exists()
        content = (temp_project / "README.md").read_text()
        assert "test" in content

    def test_gitignore_created(self, temp_project):
        """Create .gitignore"""
        generate_gitignore(temp_project)
        
        assert (temp_project / ".gitignore").exists()
        content = (temp_project / ".gitignore").read_text()
        assert "venv" in content
        assert "__pycache__" in content
