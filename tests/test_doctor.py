"""Tests for doctor command."""

import pytest
import shutil
from pathlib import Path

from src.commands.doctor import Doctor, Severity, run_doctor


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project directory."""
    project_path = tmp_path / "test_project"
    project_path.mkdir()
    return project_path


@pytest.fixture
def project_with_venv(temp_project):
    """Create project with venv inside."""
    venv_path = temp_project / "venv"
    venv_path.mkdir()
    (venv_path / "pyvenv.cfg").write_text("home = /usr/bin/python3")
    (venv_path / "bin").mkdir()
    return temp_project


@pytest.fixture
def project_with_pycache(temp_project):
    """Create project with __pycache__ directories."""
    for subdir in ["", "src", "src/utils"]:
        pycache = temp_project / subdir / "__pycache__" if subdir else temp_project / "__pycache__"
        pycache.mkdir(parents=True, exist_ok=True)
        (pycache / "test.pyc").write_text("fake")
    return temp_project


class TestDoctorDiagnosis:
    """Tests for doctor diagnosis."""
    
    def test_empty_project_has_suggestions(self, temp_project):
        """Empty project should have suggestions."""
        doctor = Doctor(temp_project)
        report = doctor.diagnose()
        
        assert report.project_name == "test_project"
        assert report.suggestion_count > 0
    
    def test_detects_venv_inside(self, project_with_venv):
        """Should detect venv inside project as CRITICAL."""
        doctor = Doctor(project_with_venv)
        report = doctor.diagnose()
        
        critical = [i for i in report.issues if i.severity == Severity.CRITICAL]
        venv_issues = [i for i in critical if "venv" in i.title.lower()]
        
        assert len(venv_issues) >= 1
    
    def test_detects_pycache(self, project_with_pycache):
        """Should detect __pycache__ directories."""
        doctor = Doctor(project_with_pycache)
        report = doctor.diagnose()
        
        pycache_issues = [i for i in report.issues if "pycache" in i.title.lower()]
        assert len(pycache_issues) >= 1
    
    def test_detects_missing_cursorignore(self, temp_project):
        """Should suggest creating .cursorignore."""
        doctor = Doctor(temp_project)
        report = doctor.diagnose()
        
        cursorignore_issues = [i for i in report.issues if "cursorignore" in i.title.lower()]
        assert len(cursorignore_issues) >= 1
    
    def test_detects_missing_ai_include(self, temp_project):
        """Should suggest creating _AI_INCLUDE."""
        doctor = Doctor(temp_project)
        report = doctor.diagnose()
        
        ai_include_issues = [i for i in report.issues if "_AI_INCLUDE" in i.title]
        assert len(ai_include_issues) >= 1
    
    def test_detects_log_files(self, temp_project):
        """Should detect scattered .log files."""
        (temp_project / "app.log").write_text("log content" * 100)
        (temp_project / "error.log").write_text("error log content" * 100)
        
        doctor = Doctor(temp_project)
        report = doctor.diagnose()
        
        log_issues = [i for i in report.issues if ".log" in i.title]
        assert len(log_issues) >= 1
    
    def test_healthy_project_no_critical(self, temp_project):
        """A properly configured project should have no critical issues."""
        # Set up a healthy project
        (temp_project / ".cursorignore").write_text("venv/\n")
        ai_include = temp_project / "_AI_INCLUDE"
        ai_include.mkdir()
        (ai_include / "PROJECT_CONVENTIONS.md").write_text("# Conventions")
        scripts = temp_project / "scripts"
        scripts.mkdir()
        (scripts / "bootstrap.sh").write_text("#!/bin/bash\n")
        
        doctor = Doctor(temp_project)
        report = doctor.diagnose()
        
        assert report.critical_count == 0


class TestDoctorFixes:
    """Tests for doctor fix actions."""
    
    def test_fix_pycache(self, project_with_pycache):
        """Should delete all __pycache__ directories."""
        doctor = Doctor(project_with_pycache)
        report = doctor.diagnose()
        
        pycache_issue = next(i for i in report.issues if "pycache" in i.title.lower())
        result = doctor.fix_issue(pycache_issue)
        
        assert result is True
        assert len(list(project_with_pycache.rglob("__pycache__"))) == 0
    
    def test_fix_missing_cursorignore(self, temp_project):
        """Should create .cursorignore."""
        doctor = Doctor(temp_project)
        report = doctor.diagnose()
        
        issue = next(i for i in report.issues if "cursorignore" in i.title.lower())
        result = doctor.fix_issue(issue)
        
        assert result is True
        assert (temp_project / ".cursorignore").exists()
        
        # Verify content
        content = (temp_project / ".cursorignore").read_text()
        assert "venv/" in content
        assert "__pycache__" in content
    
    def test_fix_missing_ai_include(self, temp_project):
        """Should create _AI_INCLUDE folder."""
        doctor = Doctor(temp_project)
        report = doctor.diagnose()
        
        issue = next(i for i in report.issues if "_AI_INCLUDE" in i.title)
        result = doctor.fix_issue(issue)
        
        assert result is True
        assert (temp_project / "_AI_INCLUDE").is_dir()
        assert (temp_project / "_AI_INCLUDE" / "PROJECT_CONVENTIONS.md").exists()
        assert (temp_project / "_AI_INCLUDE" / "WHERE_THINGS_LIVE.md").exists()
    
    def test_fix_missing_bootstrap(self, temp_project):
        """Should create bootstrap scripts."""
        doctor = Doctor(temp_project)
        report = doctor.diagnose()
        
        issue = next(i for i in report.issues if "bootstrap" in i.title.lower())
        result = doctor.fix_issue(issue)
        
        assert result is True
        assert (temp_project / "scripts" / "bootstrap.sh").exists()
        assert (temp_project / "scripts" / "bootstrap.ps1").exists()
    
    def test_fix_log_files(self, temp_project):
        """Should delete scattered .log files."""
        (temp_project / "app.log").write_text("log content")
        (temp_project / "error.log").write_text("error content")
        
        doctor = Doctor(temp_project)
        report = doctor.diagnose()
        
        issue = next(i for i in report.issues if ".log" in i.title)
        result = doctor.fix_issue(issue)
        
        assert result is True
        assert not (temp_project / "app.log").exists()
        assert not (temp_project / "error.log").exists()
    
    def test_fix_venv_inside(self, project_with_venv):
        """Should delete venv inside project."""
        doctor = Doctor(project_with_venv)
        report = doctor.diagnose()
        
        venv_issue = next(i for i in report.issues if "venv" in i.title.lower() and i.severity == Severity.CRITICAL)
        result = doctor.fix_issue(venv_issue)
        
        assert result is True
        assert not (project_with_venv / "venv").exists()


class TestDoctorBackup:
    """Tests for backup functionality."""
    
    def test_creates_backup(self, temp_project):
        """Should create backup archive."""
        (temp_project / "test.py").write_text("print('hello')")
        
        doctor = Doctor(temp_project)
        backup_path = doctor.create_backup()
        
        assert backup_path.exists()
        assert backup_path.suffix == ".gz"
        assert "backup" in backup_path.name
    
    def test_backup_excludes_venv(self, project_with_venv):
        """Backup should exclude venv directory."""
        import tarfile
        
        doctor = Doctor(project_with_venv)
        backup_path = doctor.create_backup()
        
        with tarfile.open(backup_path, "r:gz") as tar:
            names = tar.getnames()
            assert not any("venv" in name for name in names)


class TestDoctorReport:
    """Tests for diagnostic report."""
    
    def test_report_properties(self, temp_project):
        """Report should calculate counts correctly."""
        # Add various issues
        (temp_project / "venv").mkdir()
        (temp_project / "venv" / "pyvenv.cfg").write_text("home = /usr/bin/python3")
        (temp_project / "venv" / "bin").mkdir()
        (temp_project / "__pycache__").mkdir()
        
        doctor = Doctor(temp_project)
        report = doctor.diagnose()
        
        # Should have at least 1 critical (venv) and 1 warning (pycache)
        assert report.critical_count >= 1
        assert report.warning_count >= 1
        
        # Total should match individual counts
        total = report.critical_count + report.warning_count + report.suggestion_count
        assert total == len(report.issues)
    
    def test_token_estimation(self, temp_project):
        """Should estimate tokens for project."""
        # Create some Python files
        (temp_project / "main.py").write_text("print('hello world')" * 100)
        (temp_project / "utils.py").write_text("def helper(): pass" * 100)
        
        doctor = Doctor(temp_project)
        report = doctor.diagnose()
        
        # Should have some tokens
        assert report.total_tokens > 0
