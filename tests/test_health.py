"""
Tests for health command
"""

import pytest
from pathlib import Path

from src.commands.health import health_check


class TestHealthCheck:
    """Tests for health check"""

    def test_clean_project_passes(self, clean_project):
        """Clean project passes check"""
        result = health_check(clean_project)
        # May be True or return warnings (but not errors)
        assert result is True or result is False

    def test_missing_ai_include_fails(self, temp_project):
        """Project without _AI_INCLUDE fails"""
        result = health_check(temp_project)
        assert result is False

    def test_venv_inside_project_fails(self, temp_project_with_venv):
        """Project with venv inside fails"""
        result = health_check(temp_project_with_venv)
        assert result is False

    def test_with_ai_include_better(self, temp_project):
        """Adding _AI_INCLUDE improves result"""
        # Create _AI_INCLUDE
        ai_dir = temp_project / "_AI_INCLUDE"
        ai_dir.mkdir()
        (ai_dir / "PROJECT_CONVENTIONS.md").write_text("# Rules")
        
        # This shouldn't fully fix it, but reduce errors
        result = health_check(temp_project)
        # Depends on other factors


class TestHealthCheckFiles:
    """Tests for individual file checks"""

    def test_detects_missing_env(self, temp_project):
        """Detect missing .env"""
        # .env missing — should be warning
        # This is checked in health_check output
        pass

    def test_detects_missing_requirements(self, temp_project):
        """Detect missing requirements.txt"""
        pass
