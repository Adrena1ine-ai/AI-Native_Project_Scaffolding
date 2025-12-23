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
)
from src.generators.git import generate_gitignore


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
        (temp_project / "scripts").mkdir()
        generate_bootstrap_sh(temp_project, "test")
        
        path = temp_project / "scripts" / "bootstrap.sh"
        assert path.exists()
        content = path.read_text()
        assert "_venvs" in content
        assert "#!/" in content

    def test_bootstrap_ps1_created(self, temp_project):
        """Create bootstrap.ps1"""
        (temp_project / "scripts").mkdir()
        generate_bootstrap_ps1(temp_project, "test")
        
        path = temp_project / "scripts" / "bootstrap.ps1"
        assert path.exists()
        content = path.read_text()
        assert "_venvs" in content

    def test_context_switcher_created(self, temp_project):
        """Create context.py"""
        (temp_project / "scripts").mkdir()
        generate_context_switcher(temp_project)
        
        path = temp_project / "scripts" / "context.py"
        assert path.exists()
        content = path.read_text()
        assert "MODULES" in content
        assert "def update_ignore" in content

    def test_health_check_created(self, temp_project):
        """Create health_check.sh"""
        (temp_project / "scripts").mkdir()
        generate_health_check(temp_project, "test")
        
        path = temp_project / "scripts" / "health_check.sh"
        assert path.exists()
        content = path.read_text()
        assert "Health Check" in content

    def test_check_repo_clean_created(self, temp_project):
        """Create check_repo_clean.sh"""
        (temp_project / "scripts").mkdir()
        generate_check_repo_clean(temp_project)
        
        path = temp_project / "scripts" / "check_repo_clean.sh"
        assert path.exists()
        content = path.read_text()
        assert "venv" in content
        assert "site-packages" in content


class TestDocker:
    """Tests for Docker file generation"""

    def test_dockerfile_bot(self, temp_project):
        """Dockerfile for bot template"""
        generate_dockerfile(temp_project, "test", "bot")
        
        assert (temp_project / "Dockerfile").exists()
        content = (temp_project / "Dockerfile").read_text()
        assert "bot/main.py" in content

    def test_dockerfile_fastapi(self, temp_project):
        """Dockerfile for fastapi template"""
        generate_dockerfile(temp_project, "test", "fastapi")
        
        content = (temp_project / "Dockerfile").read_text()
        assert "uvicorn" in content

    def test_docker_compose_created(self, temp_project):
        """Create docker-compose.yml"""
        generate_docker_compose(temp_project, "test", "bot")
        
        assert (temp_project / "docker-compose.yml").exists()
        content = (temp_project / "docker-compose.yml").read_text()
        assert "test" in content
        assert "services:" in content

    def test_dockerignore_created(self, temp_project):
        """Create .dockerignore"""
        generate_dockerignore(temp_project, "test")
        
        assert (temp_project / ".dockerignore").exists()
        content = (temp_project / ".dockerignore").read_text()
        assert "venv" in content
        assert "__pycache__" in content


class TestCICD:
    """Tests for CI/CD file generation"""

    def test_ci_workflow_created(self, temp_project):
        """Create ci.yml"""
        generate_ci_workflow(temp_project, "test")
        
        path = temp_project / ".github" / "workflows" / "ci.yml"
        assert path.exists()
        content = path.read_text()
        assert "CI" in content
        assert "pytest" in content

    def test_cd_workflow_created(self, temp_project):
        """Create cd.yml"""
        generate_cd_workflow(temp_project, "test")
        
        path = temp_project / ".github" / "workflows" / "cd.yml"
        assert path.exists()
        content = path.read_text()
        assert "Deploy" in content

    def test_pre_commit_config_created(self, temp_project):
        """Create .pre-commit-config.yaml"""
        (temp_project / "scripts").mkdir()
        generate_pre_commit_config(temp_project, "test")
        
        assert (temp_project / ".pre-commit-config.yaml").exists()
        content = (temp_project / ".pre-commit-config.yaml").read_text()
        assert "repos:" in content
        assert "ruff" in content

    def test_dependabot_created(self, temp_project):
        """Create dependabot.yml"""
        generate_dependabot(temp_project)
        
        path = temp_project / ".github" / "dependabot.yml"
        assert path.exists()
        content = path.read_text()
        assert "pip" in content


class TestProjectFiles:
    """Tests for project file generation"""

    def test_requirements_bot(self, temp_project):
        """requirements.txt for bot"""
        generate_requirements(temp_project, "test", "bot")
        
        assert (temp_project / "requirements.txt").exists()
        content = (temp_project / "requirements.txt").read_text()
        assert "aiogram" in content

    def test_requirements_fastapi(self, temp_project):
        """requirements.txt for fastapi"""
        generate_requirements(temp_project, "test", "fastapi")
        
        content = (temp_project / "requirements.txt").read_text()
        assert "fastapi" in content
        assert "uvicorn" in content

    def test_requirements_parser(self, temp_project):
        """requirements.txt for parser"""
        generate_requirements(temp_project, "test", "parser")
        
        content = (temp_project / "requirements.txt").read_text()
        assert "httpx" in content or "beautifulsoup4" in content

    def test_config_py_created(self, temp_project):
        """Create config.py"""
        generate_config_py(temp_project, "test", "bot")
        
        assert (temp_project / "config.py").exists()
        content = (temp_project / "config.py").read_text()
        assert "Settings" in content or "config" in content.lower()

    def test_env_example_created(self, temp_project):
        """Create .env.example"""
        generate_env_example(temp_project, "test", "bot")
        
        assert (temp_project / ".env.example").exists()
        content = (temp_project / ".env.example").read_text()
        assert "BOT_TOKEN" in content

    def test_readme_created(self, temp_project):
        """Create README.md"""
        generate_readme(temp_project, "test", "bot")
        
        assert (temp_project / "README.md").exists()
        content = (temp_project / "README.md").read_text()
        assert "test" in content
        assert "bootstrap" in content.lower()

    def test_gitignore_created(self, temp_project):
        """Create .gitignore"""
        generate_gitignore(temp_project, "test")
        
        assert (temp_project / ".gitignore").exists()
        content = (temp_project / ".gitignore").read_text()
        assert "venv" in content
        assert "__pycache__" in content
        assert ".env" in content
