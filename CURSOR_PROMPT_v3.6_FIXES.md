# AI Toolkit v3.6 — Fixes, Tests & Compatibility

## Context
Read these files first to understand current implementation:
```
@src/commands/doctor.py
@src/utils/heavy_mover.py
@src/utils/token_scanner.py
@src/utils/fox_trace_map.py
@src/cli.py
@tests/test_deep_clean_integration.py
```

---

## TASK 1: Path Compatibility (CRITICAL)

### Problem
The external storage path was changed from:
- **OLD:** `../_data/PROJECT_NAME/LARGE_TOKENS/`
- **NEW:** `../PROJECT_NAME_data/`

This breaks compatibility with projects that already used Deep Clean with the old path.

### Solution
Update `src/utils/heavy_mover.py` to support BOTH paths with automatic fallback:

```python
def get_external_dir(project_path: Path, create: bool = True) -> Path:
    """
    Get external storage directory for project.
    
    Supports both old and new path formats for backward compatibility:
    - NEW: ../PROJECT_NAME_data/
    - OLD: ../_data/PROJECT_NAME/LARGE_TOKENS/
    
    Logic:
    1. If OLD path exists and has files → use OLD (backward compat)
    2. Otherwise → use NEW path
    
    Args:
        project_path: Path to project root
        create: If True, create directory if not exists
    
    Returns:
        Path to external storage directory
    """
    project_name = project_path.resolve().name
    
    # New simplified path
    new_path = project_path.parent / f"{project_name}_data"
    
    # Old path (for backward compatibility)
    old_path = project_path.parent / "_data" / project_name / "LARGE_TOKENS"
    
    # Check if old path exists and has content
    if old_path.exists():
        # Check if it has files (not just empty dirs)
        has_files = any(old_path.rglob("*"))
        if has_files:
            return old_path  # Use old path for existing projects
    
    # Use new path for new projects
    if create:
        new_path.mkdir(parents=True, exist_ok=True)
    
    return new_path


def get_manifest_path(project_path: Path) -> Optional[Path]:
    """
    Find manifest.json in either old or new external storage.
    
    Returns:
        Path to manifest.json or None if not found
    """
    project_name = project_path.resolve().name
    
    # Check new path first
    new_manifest = project_path.parent / f"{project_name}_data" / "manifest.json"
    if new_manifest.exists():
        return new_manifest
    
    # Check old path
    old_manifest = project_path.parent / "_data" / project_name / "LARGE_TOKENS" / "manifest.json"
    if old_manifest.exists():
        return old_manifest
    
    return None


def get_garbage_dir(project_path: Path, create: bool = True) -> Path:
    """
    Get garbage directory for temporary/old files.
    
    Path: ../PROJECT_NAME_garbage_for_removal/
    """
    project_name = project_path.resolve().name
    garbage_path = project_path.parent / f"{project_name}_garbage_for_removal"
    
    if create:
        garbage_path.mkdir(parents=True, exist_ok=True)
    
    return garbage_path
```

### Update restore_files() function

```python
def restore_files(
    project_path: Path,
    manifest_path: Optional[Path] = None
) -> int:
    """Restore moved files back to original locations."""
    project_path = project_path.resolve()
    
    # Find manifest with compatibility check
    if manifest_path is None:
        manifest_path = get_manifest_path(project_path)
    
    if manifest_path is None or not manifest_path.exists():
        raise FileNotFoundError(
            f"Manifest not found. Checked:\n"
            f"  - ../{project_path.name}_data/manifest.json\n"
            f"  - ../_data/{project_path.name}/LARGE_TOKENS/manifest.json"
        )
    
    # ... rest of the function stays the same
```

---

## TASK 2: Garbage Clean Implementation

### Create `src/utils/garbage_cleaner.py`

```python
"""
Garbage Cleaner — Find and move temporary/old files.
Separates garbage cleanup from Deep Clean (which handles heavy files).
"""
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import shutil
import os


# Patterns for garbage files
GARBAGE_PATTERNS: Set[str] = {
    # Temp files
    "*.tmp", "*.temp", "*.bak", "*.old", "*.backup",
    "*.swp", "*.swo",  # Vim swap
    "*~",  # Backup files
    
    # Log files (old)
    "*.log.old", "*.log.1", "*.log.2", "*.log.bak",
    
    # System files
    ".DS_Store", "Thumbs.db", "desktop.ini", "ehthumbs.db",
    
    # Python
    "*.pyc", "*.pyo",
    
    # IDE
    "*.sublime-workspace",
}

# Directories to skip
SKIP_DIRS: Set[str] = {
    "venv", ".venv", "env", ".env",
    "node_modules",
    "__pycache__", ".pytest_cache", ".mypy_cache",
    ".git", ".svn", ".hg",
    ".idea", ".vscode",
    "_data", "_venvs", "_artifacts",
}

# Max age for log files (in days)
LOG_MAX_AGE_DAYS = 30


@dataclass
class GarbageFile:
    """Represents a garbage file to be cleaned."""
    path: Path
    relative_path: str
    size_bytes: int
    reason: str  # Why it's garbage
    age_days: Optional[int] = None


@dataclass
class GarbageCleanResult:
    """Result of garbage cleaning operation."""
    project_path: Path
    garbage_dir: Path
    files_found: List[GarbageFile] = field(default_factory=list)
    files_moved: List[GarbageFile] = field(default_factory=list)
    files_failed: List[Tuple[str, str]] = field(default_factory=list)
    
    @property
    def total_size(self) -> int:
        return sum(f.size_bytes for f in self.files_found)
    
    @property
    def moved_size(self) -> int:
        return sum(f.size_bytes for f in self.files_moved)


def is_old_log(file_path: Path, max_age_days: int = LOG_MAX_AGE_DAYS) -> bool:
    """Check if a log file is older than max_age_days."""
    if not file_path.suffix == ".log":
        return False
    
    try:
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        age = datetime.now() - mtime
        return age.days > max_age_days
    except (OSError, IOError):
        return False


def get_file_age_days(file_path: Path) -> Optional[int]:
    """Get file age in days."""
    try:
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        return (datetime.now() - mtime).days
    except (OSError, IOError):
        return None


def scan_garbage(
    project_path: Path,
    include_old_logs: bool = True,
    log_max_age: int = LOG_MAX_AGE_DAYS
) -> List[GarbageFile]:
    """
    Scan project for garbage files.
    
    Args:
        project_path: Project root
        include_old_logs: If True, include log files older than log_max_age
        log_max_age: Max age for log files in days
    
    Returns:
        List of garbage files found
    """
    project_path = project_path.resolve()
    garbage_files = []
    
    for root, dirs, files in os.walk(project_path):
        # Filter out skip directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        
        root_path = Path(root)
        
        for file_name in files:
            file_path = root_path / file_name
            reason = None
            
            # Check against patterns
            for pattern in GARBAGE_PATTERNS:
                if file_path.match(pattern):
                    reason = f"Matches pattern: {pattern}"
                    break
            
            # Check for old logs
            if reason is None and include_old_logs and is_old_log(file_path, log_max_age):
                reason = f"Log file older than {log_max_age} days"
            
            if reason:
                try:
                    garbage_files.append(GarbageFile(
                        path=file_path,
                        relative_path=str(file_path.relative_to(project_path)),
                        size_bytes=file_path.stat().st_size,
                        reason=reason,
                        age_days=get_file_age_days(file_path)
                    ))
                except (OSError, IOError):
                    continue
    
    # Sort by size (largest first)
    garbage_files.sort(key=lambda x: x.size_bytes, reverse=True)
    
    return garbage_files


def clean_garbage(
    project_path: Path,
    dry_run: bool = False,
    include_old_logs: bool = True,
    log_max_age: int = LOG_MAX_AGE_DAYS
) -> GarbageCleanResult:
    """
    Find and move garbage files to garbage directory.
    
    Args:
        project_path: Project root
        dry_run: If True, don't actually move files
        include_old_logs: Include old log files
        log_max_age: Max age for logs in days
    
    Returns:
        GarbageCleanResult with statistics
    """
    from .heavy_mover import get_garbage_dir
    
    project_path = project_path.resolve()
    garbage_dir = get_garbage_dir(project_path, create=not dry_run)
    
    result = GarbageCleanResult(
        project_path=project_path,
        garbage_dir=garbage_dir
    )
    
    # Scan for garbage
    result.files_found = scan_garbage(
        project_path, 
        include_old_logs=include_old_logs,
        log_max_age=log_max_age
    )
    
    if dry_run:
        return result
    
    # Move files
    for gf in result.files_found:
        try:
            # Preserve directory structure
            dest_path = garbage_dir / gf.relative_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(gf.path), str(dest_path))
            result.files_moved.append(gf)
            
        except Exception as e:
            result.files_failed.append((gf.relative_path, str(e)))
    
    return result


def format_garbage_report(result: GarbageCleanResult, dry_run: bool = False) -> str:
    """Format garbage clean result as readable report."""
    lines = []
    
    lines.append("╔══════════════════════════════════════════════════════════════════╗")
    if dry_run:
        lines.append("║  🗑️  GARBAGE SCAN — Preview (Dry Run)                           ║")
    else:
        lines.append("║  🗑️  GARBAGE CLEAN — Files Moved                                ║")
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    
    lines.append(f"║  Project: {result.project_path.name:<55}║")
    
    total_kb = result.total_size / 1024
    lines.append(f"║  Garbage Found: {len(result.files_found)} files ({total_kb:.1f} KB){' '*(35-len(f'{total_kb:.1f}'))}║")
    
    if result.files_found:
        lines.append("╠══════════════════════════════════════════════════════════════════╣")
        lines.append("║  FILES:                                                          ║")
        
        for i, gf in enumerate(result.files_found[:10]):
            prefix = "└─" if i == min(len(result.files_found), 10) - 1 else "├─"
            size_str = f"{gf.size_bytes/1024:.1f}KB"
            path_str = gf.relative_path[:40]
            lines.append(f"║  {prefix} {path_str:<40} {size_str:>8}    ║")
        
        if len(result.files_found) > 10:
            lines.append(f"║  ... and {len(result.files_found) - 10} more files{' '*45}║")
    
    if not dry_run:
        lines.append("╠══════════════════════════════════════════════════════════════════╣")
        moved_kb = result.moved_size / 1024
        lines.append(f"║  ✅ Moved: {len(result.files_moved)} files ({moved_kb:.1f} KB){' '*(39-len(f'{moved_kb:.1f}'))}║")
        lines.append(f"║  📁 Location: {str(result.garbage_dir.name):<51}║")
        
        if result.files_failed:
            lines.append(f"║  ❌ Failed: {len(result.files_failed)} files{' '*46}║")
    
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    if dry_run:
        lines.append("║  💡 Run without --dry-run to move these files                   ║")
    else:
        lines.append("║  💡 Review and delete: " + str(result.garbage_dir.name)[:40] + " "*(22-len(str(result.garbage_dir.name)[:40])) + "║")
    lines.append("╚══════════════════════════════════════════════════════════════════╝")
    
    return "\n".join(lines)
```

---

## TASK 3: Integrate Garbage Clean into Doctor Command

### Update `src/commands/doctor.py`

Add at the top:
```python
from ..utils.garbage_cleaner import clean_garbage, format_garbage_report
```

Add new function:
```python
def run_garbage_clean(
    project_path: Path,
    auto: bool = False,
    dry_run: bool = False,
    include_old_logs: bool = True,
    log_max_age: int = 30
) -> bool:
    """
    Run garbage cleanup — move temp/backup files to garbage folder.
    """
    project_path = project_path.resolve()
    
    print(COLORS.info(f"\n🗑️  GARBAGE CLEAN — {project_path.name}"))
    print(COLORS.info(f"   Mode: {'Dry Run' if dry_run else 'Live'}\n"))
    
    # Scan/clean
    result = clean_garbage(
        project_path,
        dry_run=dry_run,
        include_old_logs=include_old_logs,
        log_max_age=log_max_age
    )
    
    if not result.files_found:
        print(COLORS.success("\n✅ No garbage files found! Project is clean."))
        return True
    
    # Show report
    print(format_garbage_report(result, dry_run=dry_run))
    
    # If dry run or already done, return
    if dry_run:
        return True
    
    # Confirm if not auto
    if not auto and result.files_found:
        print(f"\n🔴 Found {len(result.files_found)} garbage files")
        print(f"   Will move to: {result.garbage_dir.name}/")
        print()
        
        try:
            confirm = input("   Continue? [y/N]: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n   Cancelled.")
            return False
        
        if confirm != 'y':
            print("   Cancelled.")
            return False
        
        # Run actual clean
        result = clean_garbage(
            project_path,
            dry_run=False,
            include_old_logs=include_old_logs,
            log_max_age=log_max_age
        )
        print(format_garbage_report(result, dry_run=False))
    
    # Update documentation after cleanup
    if result.files_moved:
        print(COLORS.info("\n📝 Updating documentation..."))
        try:
            from .status import cmd_status
            import argparse
            args = argparse.Namespace(path=str(project_path), preview=False)
            cmd_status(args)
            print(COLORS.success("   ✅ Documentation updated"))
        except Exception as e:
            print(COLORS.warning(f"   ⚠️  Could not update docs: {e}"))
    
    return True
```

### Update cmd_doctor() to handle --garbage-clean:

```python
def cmd_doctor(args):
    """CLI entry point for doctor command."""
    # Get project path
    if hasattr(args, 'path') and args.path:
        project_path = Path(args.path).resolve()
    else:
        project_path = Path.cwd()
    
    if not project_path.exists():
        print(COLORS.error(f"❌ Path not found: {project_path}"))
        return False
    
    # Check for restore mode
    if hasattr(args, 'restore') and args.restore:
        return run_restore(project_path)
    
    # Check for garbage-clean mode
    if hasattr(args, 'garbage_clean') and args.garbage_clean:
        auto = getattr(args, 'auto', False)
        dry_run = getattr(args, 'dry_run', False)
        return run_garbage_clean(project_path, auto=auto, dry_run=dry_run)
    
    # Check for deep-clean mode
    if hasattr(args, 'deep_clean') and args.deep_clean:
        threshold = getattr(args, 'threshold', 1000)
        auto = getattr(args, 'auto', False)
        dry_run = getattr(args, 'dry_run', False)
        no_patch = getattr(args, 'no_patch', False)
        
        return run_deep_clean(
            project_path,
            threshold=threshold,
            auto=auto,
            dry_run=dry_run,
            patch_code=not no_patch
        )
    
    # Existing doctor logic
    auto = hasattr(args, 'auto') and args.auto
    report_only = hasattr(args, 'report') and args.report
    
    return run_doctor(project_path, auto=auto, report_only=report_only)
```

---

## TASK 4: Update CLI Arguments

### Update `src/cli.py` — add garbage-clean flag:

```python
# In doctor_parser section, add:
doctor_parser.add_argument(
    "--garbage-clean", "-G",
    action="store_true",
    dest="garbage_clean",
    help="Move temporary/backup files to garbage folder"
)
```

---

## TASK 5: Create Tests for Garbage Clean

### Create `tests/test_garbage_cleaner.py`:

```python
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
        assert "Preview" in report or "dry-run" in report.lower()
    
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
```

---

## TASK 6: Update Tests for Path Compatibility

### Update `tests/test_heavy_mover.py`:

Add these tests:

```python
class TestPathCompatibility:
    def test_uses_new_path_for_new_projects(self, temp_project, heavy_files):
        """New projects should use simplified path."""
        result = move_heavy_files(temp_project, heavy_files)
        
        # Should use new path format
        assert "_data" not in str(result.external_dir)
        assert f"{temp_project.name}_data" in str(result.external_dir)
    
    def test_respects_old_path_if_exists(self, temp_project, heavy_files):
        """Projects with old path should continue using it."""
        from src.utils.heavy_mover import get_external_dir
        
        # Create old-style directory with content
        old_path = temp_project.parent / "_data" / temp_project.name / "LARGE_TOKENS"
        old_path.mkdir(parents=True)
        (old_path / "existing_file.json").write_text("{}")
        
        # Should detect and use old path
        ext_dir = get_external_dir(temp_project)
        assert "_data" in str(ext_dir)
        assert "LARGE_TOKENS" in str(ext_dir)
    
    def test_manifest_found_in_old_path(self, temp_project):
        """Should find manifest in old-style path."""
        from src.utils.heavy_mover import get_manifest_path
        
        # Create old-style manifest
        old_path = temp_project.parent / "_data" / temp_project.name / "LARGE_TOKENS"
        old_path.mkdir(parents=True)
        (old_path / "manifest.json").write_text('{"project": "test"}')
        
        manifest = get_manifest_path(temp_project)
        assert manifest is not None
        assert manifest.exists()
    
    def test_manifest_found_in_new_path(self, temp_project):
        """Should find manifest in new-style path."""
        from src.utils.heavy_mover import get_manifest_path
        
        # Create new-style manifest
        new_path = temp_project.parent / f"{temp_project.name}_data"
        new_path.mkdir(parents=True)
        (new_path / "manifest.json").write_text('{"project": "test"}')
        
        manifest = get_manifest_path(temp_project)
        assert manifest is not None
        assert manifest.exists()
```

---

## TASK 7: Update Progress Indicators

### Add progress display to heavy operations in `src/utils/token_scanner.py`:

```python
def scan_project(
    project_path: Path,
    threshold: int = 1000,
    include_code: bool = False,
    extract_schemas: bool = True,
    show_progress: bool = True  # NEW parameter
) -> ScanResult:
    """Scan project for heavy files with optional progress display."""
    # ... existing setup code ...
    
    # Count total files first for progress
    all_files = list(project_path.rglob("*"))
    total_files = len([f for f in all_files if f.is_file()])
    processed = 0
    
    for root, dirs, files in os.walk(project_path):
        # ... existing filter code ...
        
        for file_name in files:
            processed += 1
            
            if show_progress and processed % 50 == 0:
                pct = (processed / total_files) * 100 if total_files > 0 else 0
                print(f"\r   Scanning: {processed}/{total_files} files ({pct:.0f}%)...", end="", flush=True)
            
            # ... rest of existing code ...
    
    if show_progress:
        print(f"\r   Scanning: {total_files}/{total_files} files (100%)     ")
    
    return result
```

---

## Summary of Changes

1. **Path Compatibility** (`heavy_mover.py`):
   - `get_external_dir()` — supports old and new paths
   - `get_manifest_path()` — finds manifest in either location
   - `get_garbage_dir()` — new function for garbage directory

2. **Garbage Cleaner** (`garbage_cleaner.py`):
   - `scan_garbage()` — find garbage files
   - `clean_garbage()` — move to garbage folder
   - `format_garbage_report()` — readable output

3. **Doctor Command** (`doctor.py`):
   - `run_garbage_clean()` — new function
   - Updated `cmd_doctor()` to handle `--garbage-clean`

4. **CLI** (`cli.py`):
   - Added `--garbage-clean` / `-G` flag

5. **Tests**:
   - `test_garbage_cleaner.py` — 20+ new tests
   - `test_heavy_mover.py` — path compatibility tests

## Verification

```bash
# Run all new tests
pytest tests/test_garbage_cleaner.py -v
pytest tests/test_heavy_mover.py -v -k "compat"

# Test garbage clean
python main.py doctor . --garbage-clean --dry-run

# Test path compatibility
python -c "
from src.utils.heavy_mover import get_external_dir, get_manifest_path
from pathlib import Path
print('External dir:', get_external_dir(Path('.'), create=False))
print('Manifest:', get_manifest_path(Path('.')))
"
```
