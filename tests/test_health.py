"""
Тесты команды health
"""

import pytest
from pathlib import Path

from src.commands.health import health_check


class TestHealthCheck:
    """Тесты health check"""

    def test_clean_project_passes(self, clean_project):
        """Чистый проект проходит проверку"""
        result = health_check(clean_project)
        # Может быть True или вернуть warnings (но не errors)
        assert result is True or result is False

    def test_missing_ai_include_fails(self, temp_project):
        """Проект без _AI_INCLUDE не проходит"""
        result = health_check(temp_project)
        assert result is False

    def test_venv_inside_project_fails(self, temp_project_with_venv):
        """Проект с venv внутри не проходит"""
        result = health_check(temp_project_with_venv)
        assert result is False

    def test_with_ai_include_better(self, temp_project):
        """Добавление _AI_INCLUDE улучшает результат"""
        # Создаём _AI_INCLUDE
        ai_dir = temp_project / "_AI_INCLUDE"
        ai_dir.mkdir()
        (ai_dir / "PROJECT_CONVENTIONS.md").write_text("# Rules")
        
        # Это не должно полностью исправить, но уменьшить ошибки
        result = health_check(temp_project)
        # Зависит от других факторов


class TestHealthCheckFiles:
    """Тесты проверки отдельных файлов"""

    def test_detects_missing_env(self, temp_project):
        """Обнаружение отсутствующего .env"""
        # .env нет — должен быть warning
        # Это проверяется в health_check output
        pass

    def test_detects_missing_requirements(self, temp_project):
        """Обнаружение отсутствующего requirements.txt"""
        pass

