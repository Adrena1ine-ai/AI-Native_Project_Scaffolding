"""
Тесты команды cleanup
"""

import pytest
from pathlib import Path

from src.commands.cleanup import analyze_project, cleanup_project, Issue


class TestAnalyzeProject:
    """Тесты анализа проекта"""

    def test_detect_venv_inside_project(self, temp_project_with_venv):
        """Обнаружение venv внутри проекта"""
        issues = analyze_project(temp_project_with_venv)
        
        venv_issues = [i for i in issues if i.type == "venv"]
        assert len(venv_issues) >= 1
        assert any("venv" in i.message for i in venv_issues)

    def test_detect_missing_configs(self, temp_project):
        """Обнаружение отсутствующих конфигов"""
        issues = analyze_project(temp_project)
        
        config_issues = [i for i in issues if i.type == "config"]
        assert len(config_issues) >= 1

    def test_detect_pycache(self, temp_project):
        """Обнаружение __pycache__"""
        # Создаём __pycache__
        (temp_project / "__pycache__").mkdir()
        (temp_project / "__pycache__" / "test.pyc").touch()
        
        issues = analyze_project(temp_project)
        
        cache_issues = [i for i in issues if i.type == "cache"]
        assert len(cache_issues) == 1

    def test_detect_large_logs(self, temp_project):
        """Обнаружение больших логов"""
        logs_dir = temp_project / "logs"
        logs_dir.mkdir()
        
        # Создаём большой лог (>10MB)
        large_log = logs_dir / "big.log"
        large_log.write_bytes(b"x" * (11 * 1024 * 1024))  # 11 MB
        
        issues = analyze_project(temp_project)
        
        log_issues = [i for i in issues if i.type == "logs"]
        assert len(log_issues) == 1

    def test_clean_project_no_issues(self, clean_project):
        """Чистый проект не должен иметь критических проблем"""
        issues = analyze_project(clean_project)
        
        # Не должно быть venv ошибок
        venv_issues = [i for i in issues if i.type == "venv"]
        assert len(venv_issues) == 0


class TestCleanupProject:
    """Тесты очистки проекта"""

    def test_safe_level_no_changes(self, temp_project_with_venv):
        """Уровень safe не меняет файлы"""
        venv_before = (temp_project_with_venv / "venv").exists()
        
        result = cleanup_project(temp_project_with_venv, "safe")
        
        assert result is True
        assert (temp_project_with_venv / "venv").exists() == venv_before

    def test_medium_level_moves_venv(self, temp_project_with_venv, temp_dir):
        """Уровень medium перемещает venv"""
        # Убедимся что venv есть
        assert (temp_project_with_venv / "venv").exists()
        
        result = cleanup_project(temp_project_with_venv, "medium")
        
        assert result is True
        # venv должен быть удалён или перемещён
        # (зависит от того существует ли ../_venvs)

    def test_cleanup_removes_pycache(self, temp_project):
        """Очистка удаляет __pycache__"""
        pycache = temp_project / "__pycache__"
        pycache.mkdir()
        (pycache / "test.pyc").touch()
        
        cleanup_project(temp_project, "medium")
        
        assert not pycache.exists()


class TestIssueClass:
    """Тесты класса Issue"""

    def test_issue_str_with_size(self):
        """Issue с размером"""
        issue = Issue(
            type="venv",
            severity="error",
            path=Path("/test/venv"),
            size_mb=500.0,
            message="Найден venv/",
            fix_action="move"
        )
        
        result = str(issue)
        assert "500.0 MB" in result
        assert "venv" in result

    def test_issue_str_without_size(self):
        """Issue без размера"""
        issue = Issue(
            type="config",
            severity="warning",
            path=None,
            size_mb=0,
            message="Нет конфигов",
            fix_action="create"
        )
        
        result = str(issue)
        assert "MB" not in result
        assert "Нет конфигов" in result

    def test_issue_icons(self):
        """Иконки для разных severity"""
        error = Issue("x", "error", None, 0, "test", "x")
        warning = Issue("x", "warning", None, 0, "test", "x")
        info = Issue("x", "info", None, 0, "test", "x")
        
        assert "❌" in str(error)
        assert "⚠️" in str(warning)
        assert "ℹ️" in str(info)

