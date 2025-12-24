"""
🧹 Cleaner — Archive artifacts and garbage files
"""

from __future__ import annotations

import shutil
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass


# Safe patterns to archive (not delete, move to _AI_ARCHIVE)
ARCHIVE_PATTERNS = {
    # Pattern: (description, is_dir)
    "*.log": ("Log file", False),
    "*.tmp": ("Temporary file", False),
    "*.bak": ("Backup file", False),
    "*.swp": ("Vim swap file", False),
    "*.swo": ("Vim swap file", False),
    "*~": ("Editor backup", False),
    "Thumbs.db": ("Windows thumbnail cache", False),
    ".DS_Store": ("macOS metadata", False),
    "__pycache__": ("Python cache", True),
    ".pytest_cache": ("Pytest cache", True),
    ".mypy_cache": ("Mypy cache", True),
    ".ruff_cache": ("Ruff cache", True),
    "*.pyc": ("Compiled Python", False),
    "*.pyo": ("Optimized Python", False),
}

# Directories to never touch
PROTECTED_DIRS = {".git", ".venv", "venv", "node_modules", "_AI_ARCHIVE"}


@dataclass
class ArchiveResult:
    """Result of archive operation"""
    count_moved: int
    size_freed: int  # bytes
    moved_files: list[tuple[str, str]]  # (relative_path, reason)
    
    @property
    def formatted_size(self) -> str:
        """Format size with appropriate unit"""
        if self.size_freed >= 1_000_000:
            return f"{self.size_freed / 1_000_000:.1f}MB"
        elif self.size_freed >= 1_000:
            return f"{self.size_freed / 1_000:.1f}KB"
        return f"{self.size_freed}B"


def matches_pattern(name: str, pattern: str) -> bool:
    """Check if filename matches a glob-like pattern"""
    import fnmatch
    return fnmatch.fnmatch(name, pattern)


def get_file_size(path: Path) -> int:
    """Get file or directory size in bytes"""
    if path.is_file():
        try:
            return path.stat().st_size
        except OSError:
            return 0
    elif path.is_dir():
        total = 0
        try:
            for p in path.rglob("*"):
                if p.is_file():
                    try:
                        total += p.stat().st_size
                    except OSError:
                        pass
        except OSError:
            pass
        return total
    return 0


def archive_artifacts(project_path: Path) -> ArchiveResult:
    """
    Archive garbage files to _AI_ARCHIVE folder
    
    Args:
        project_path: Path to project root
        
    Returns:
        ArchiveResult with count, size, and file list
    """
    project_path = Path(project_path).resolve()
    archive_dir = project_path / "_AI_ARCHIVE"
    
    moved_files: list[tuple[str, str]] = []
    count_moved = 0
    size_freed = 0
    
    # Collect files/dirs to archive
    items_to_archive: list[tuple[Path, str, bool]] = []  # (path, reason, is_dir)
    
    for dirpath, dirnames, filenames in os.walk(project_path):
        current = Path(dirpath)
        
        # Skip protected directories
        if any(p in current.parts for p in PROTECTED_DIRS):
            continue
        
        # Skip if already in archive
        try:
            current.relative_to(archive_dir)
            continue  # Inside archive, skip
        except ValueError:
            pass  # Not in archive, continue
        
        # Check directories
        dirs_to_remove = []
        for dirname in dirnames:
            if dirname in PROTECTED_DIRS:
                dirs_to_remove.append(dirname)
                continue
            
            for pattern, (reason, is_dir) in ARCHIVE_PATTERNS.items():
                if is_dir and matches_pattern(dirname, pattern):
                    items_to_archive.append((current / dirname, reason, True))
                    dirs_to_remove.append(dirname)
                    break
        
        # Don't descend into dirs we're archiving
        for d in dirs_to_remove:
            if d in dirnames:
                dirnames.remove(d)
        
        # Check files
        for filename in filenames:
            file_path = current / filename
            
            for pattern, (reason, is_dir) in ARCHIVE_PATTERNS.items():
                if not is_dir and matches_pattern(filename, pattern):
                    items_to_archive.append((file_path, reason, False))
                    break
    
    # Create archive directory if needed
    if items_to_archive:
        archive_dir.mkdir(exist_ok=True)
    
    # Move items to archive
    for item_path, reason, is_dir in items_to_archive:
        try:
            rel_path = item_path.relative_to(project_path)
            archive_dest = archive_dir / rel_path
            
            # Get size before moving
            item_size = get_file_size(item_path)
            
            # Create parent directories in archive
            archive_dest.parent.mkdir(parents=True, exist_ok=True)
            
            # Move item
            if archive_dest.exists():
                if is_dir:
                    shutil.rmtree(archive_dest)
                else:
                    archive_dest.unlink()
            
            shutil.move(str(item_path), str(archive_dest))
            
            moved_files.append((str(rel_path), reason))
            count_moved += 1
            size_freed += item_size
            
        except Exception:
            continue  # Skip on error
    
    # Generate report
    if moved_files:
        _generate_archive_report(archive_dir, moved_files)
    
    return ArchiveResult(
        count_moved=count_moved,
        size_freed=size_freed,
        moved_files=moved_files
    )


def _generate_archive_report(archive_dir: Path, moved_files: list[tuple[str, str]]) -> None:
    """Generate MOVED_FILES.md report in archive directory"""
    
    content = f'''# 📦 Archived Files

> Generated by AI Toolkit on {datetime.now().strftime("%Y-%m-%d %H:%M")}

These files were moved from the project to reduce AI context pollution.
They are preserved here and can be restored if needed.

---

## 📋 Moved Files

| File | Reason |
|------|--------|
'''
    
    for file_path, reason in sorted(moved_files):
        content += f"| `{file_path}` | {reason} |\n"
    
    content += f'''
---

## 🔄 Restore Instructions

To restore a file, move it back to its original location:

```bash
mv _AI_ARCHIVE/path/to/file path/to/file
```

Or restore everything:

```bash
cp -r _AI_ARCHIVE/* . && rm -rf _AI_ARCHIVE
```

---

*This archive can be safely deleted if files are no longer needed.*
'''
    
    report_path = archive_dir / "MOVED_FILES.md"
    report_path.write_text(content, encoding="utf-8")


# Need os import for os.walk
import os

