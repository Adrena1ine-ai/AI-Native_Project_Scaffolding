"""Tests for garbage cleaner utility."""
import pytest
from pathlib import Path
import tempfile
import shutil
from datetime import datetime, timedelta
import os

from src.utils.garbage_cleaner import (
    scan_garbage,
    clean_garbage,
    format_garbage_report,
    is_old_log,
    get_file_age_days,
    GarbageFile,
    GarbageCleanResult,
    GARBAGE_PATTERNS
)


@pytest.fixture
def temp_project():
    """Create a temporary project with garbage files."""
    temp_dir = tempfile.mkdtemp()
    project = Path(temp_dir) / "test_project"
    project.mkdir()
    
    # Create normal files
    (project / "main.py").write_text("print('hello')")
    (project / "config.json").write_text("{}")
    
    # Create garbage files
    (project / "temp_file.tmp").write_text("temporary")
    (project / "backup.bak").write_text("backup data")
    (project / "old_version.old").write_text("old version")
    (project / ".DS_Store").write_bytes(b"mac garbage")
    (project / "Thumbs.db").write_bytes(b"windows garbage")
    
    # Create subdirectory with garbage
    subdir = project / "src"
    subdir.mkdir()
    (subdir / "module.py").write_text("# module")
    (subdir / "module.py.bak").write_text("# backup")
    (subdir / "test.tmp").write_text("temp")
    
    # Create log files
    logs_dir = project / "logs"
    logs_dir.mkdir()
    (logs_dir / "app.log").write_text("current log")
    (logs_dir / "app.log.old").write_text("old log")
    (logs_dir / "app.log.1").write_text("rotated log 1")
    
    yield project
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_project_with_old_logs():
    """Create project with old log files."""
    temp_dir = tempfile.mkdtemp()
    project = Path(temp_dir) / "test_project"
    project.mkdir()
    
    # Create old log file (modify mtime)
    old_log = project / "old.log"
    old_log.write_text("old log content")
    
    # Set modification time to 60 days ago
    old_time = (datetime.now() - timedelta(days=60)).timestamp()
    os.utime(old_log, (old_time, old_time))
    
    # Create recent log file
    recent_log = project / "recent.log"
    recent_log.write_text("recent log content")
    
    yield project
    shutil.rmtree(temp_dir)


class TestIsOldLog:
    def test_old_log_detected(self, temp_project_with_old_logs):
        old_log = temp_project_with_old_logs / "old.log"
        assert is_old_log(old_log, max_age_days=30) is True
    
    def test_recent_log_not_detected(self, temp_project_with_old_logs):
        recent_log = temp_project_with_old_logs / "recent.log"
        assert is_old_log(recent_log, max_age_days=30) is False
    
    def test_non_log_file(self, temp_project):
        main_py = temp_project / "main.py"
        assert is_old_log(main_py) is False


class TestGetFileAgeDays:
    def test_returns_age(self, temp_project):
        main_py = temp_project / "main.py"
        age = get_file_age_days(main_py)
        assert age is not None
        assert age >= 0
    
    def test_nonexistent_file(self):
        age = get_file_age_days(Path("/nonexistent/file.txt"))
        assert age is None


class TestScanGarbage:
    def test_finds_tmp_files(self, temp_project):
        garbage = scan_garbage(temp_project)
        tmp_files = [g for g in garbage if g.path.suffix == ".tmp"]
        assert len(tmp_files) >= 1
    
    def test_finds_bak_files(self, temp_project):
        garbage = scan_garbage(temp_project)
        bak_files = [g for g in garbage if g.path.suffix == ".bak"]
        assert len(bak_files) >= 2  # backup.bak and module.py.bak
    
    def test_finds_system_files(self, temp_project):
        garbage = scan_garbage(temp_project)
        names = [g.path.name for g in garbage]
        assert ".DS_Store" in names
        assert "Thumbs.db" in names
    
    def test_finds_old_log_patterns(self, temp_project):
        garbage = scan_garbage(temp_project)
        old_logs = [g for g in garbage if ".log." in g.path.name]
        assert len(old_logs) >= 1
    
    def test_skips_normal_files(self, temp_project):
        garbage = scan_garbage(temp_project)
        paths = [g.relative_path for g in garbage]
        assert "main.py" not in paths
        assert "config.json" not in paths
    
    def test_includes_subdirectories(self, temp_project):
        garbage = scan_garbage(temp_project)
        subdir_garbage = [g for g in garbage if "src" in g.relative_path]
        assert len(subdir_garbage) >= 1
    
    def test_sorted_by_size(self, temp_project):
        garbage = scan_garbage(temp_project)
        if len(garbage) >= 2:
            assert garbage[0].size_bytes >= garbage[1].size_bytes


class TestCleanGarbage:
    def test_dry_run_doesnt_move(self, temp_project):
        result = clean_garbage(temp_project, dry_run=True)
        
        assert len(result.files_found) > 0
        assert len(result.files_moved) == 0
        
        # Files should still exist
        assert (temp_project / "temp_file.tmp").exists()
    
    def test_moves_garbage_files(self, temp_project):
        result = clean_garbage(temp_project, dry_run=False)
        
        assert len(result.files_moved) > 0
        
        # Files should be moved
        assert not (temp_project / "temp_file.tmp").exists()
        assert not (temp_project / "backup.bak").exists()
    
    def test_creates_garbage_dir(self, temp_project):
        result = clean_garbage(temp_project, dry_run=False)
        
        assert result.garbage_dir.exists()
        assert "garbage" in result.garbage_dir.name
    
    def test_preserves_structure(self, temp_project):
        result = clean_garbage(temp_project, dry_run=False)
        
        # Check that subdirectory structure is preserved
        subdir_garbage = result.garbage_dir / "src" / "module.py.bak"
        assert subdir_garbage.exists()
    
    def test_result_contains_stats(self, temp_project):
        result = clean_garbage(temp_project, dry_run=False)
        
        assert result.total_size > 0
        assert result.moved_size > 0


class TestFormatGarbageReport:
    def test_dry_run_format(self, temp_project):
        result = clean_garbage(temp_project, dry_run=True)
        report = format_garbage_report(result, dry_run=True)
        
        assert "GARBAGE SCAN" in report
        assert "Dry Run" in report
    
    def test_live_format(self, temp_project):
        result = clean_garbage(temp_project, dry_run=False)
        report = format_garbage_report(result, dry_run=False)
        
        assert "GARBAGE CLEAN" in report
        assert "Moved" in report


class TestGarbagePatterns:
    def test_common_patterns_exist(self):
        assert "*.tmp" in GARBAGE_PATTERNS
        assert "*.bak" in GARBAGE_PATTERNS
        assert ".DS_Store" in GARBAGE_PATTERNS
        assert "Thumbs.db" in GARBAGE_PATTERNS


class TestIntegration:
    def test_full_workflow(self, temp_project):
        # Scan
        garbage = scan_garbage(temp_project)
        initial_count = len(garbage)
        assert initial_count > 0
        
        # Clean
        result = clean_garbage(temp_project, dry_run=False)
        assert len(result.files_moved) == initial_count
        
        # Verify empty after clean
        garbage_after = scan_garbage(temp_project)
        assert len(garbage_after) == 0

