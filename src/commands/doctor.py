"""
Doctor command — Diagnose and auto-fix project issues.
The "one button fixes everything" solution.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tarfile
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional

from ..core.constants import COLORS, VERSION
from ..utils.status_generator import update_status

# Import architect module for architectural restructuring
try:
    from .architect import restructure_project, create_config_paths
    HAS_ARCHITECT = True
except ImportError:
    HAS_ARCHITECT = False
    restructure_project = None
    create_config_paths = None

# Import context map generator for automatic updates
try:
    from ..utils.context_map import write_context_map
    HAS_CONTEXT_MAP = True
except ImportError:
    HAS_CONTEXT_MAP = False
    write_context_map = None

# Protected files that Doctor should NEVER touch
PROTECTED_FILES = {
    "first manifesto.md",
    "PROJECT_STATUS.md",
    "TECHNICAL_SPECIFICATION.md",
    "README.md",
    "CURRENT_CONTEXT_MAP.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "LICENSE.md",
    ".gitignore",
    ".cursorignore",
    "pyproject.toml",
    "setup.py",
    "requirements.txt",
    "main.py",
}


def is_protected_file(file_path: Path) -> bool:
    """Check if a file is protected and should never be modified by Doctor."""
    file_name = file_path.name
    # Check exact filename
    if file_name in PROTECTED_FILES:
        return True
    # Check if it's in _AI_INCLUDE (protected directory)
    if "_AI_INCLUDE" in str(file_path):
        return True
    # Check if it's in .cursor/rules (protected directory)
    if ".cursor" in str(file_path) and "rules" in str(file_path):
        return True
    return False


class Severity(Enum):
    """Issue severity levels."""
    CRITICAL = "critical"
    WARNING = "warning"
    SUGGESTION = "suggestion"


@dataclass
class Issue:
    """Represents a single project issue."""
    id: int
    severity: Severity
    title: str
    description: str
    path: Optional[Path] = None
    tokens_impact: int = 0
    fix_function: Optional[str] = None  # Name of fix method


@dataclass
class FileTokens:
    """Token consumption for a single file."""
    path: Path
    tokens: int
    relative_path: str


@dataclass
class ChangeRecord:
    """Record of a change made by doctor."""
    action: str  # "moved", "archived", "created"
    item_type: str  # "venv", "file", "directory", "cache", "logs", "config"
    source: Optional[Path] = None
    destination: Optional[Path] = None
    size_bytes: int = 0
    description: str = ""


@dataclass
class DiagnosticReport:
    """Complete diagnostic report for a project."""
    project_path: Path
    project_name: str
    total_tokens: int
    issues: List[Issue] = field(default_factory=list)
    file_tokens: List[FileTokens] = field(default_factory=list)
    external_venv_exists: bool = False
    external_venv_path: Optional[Path] = None
    changes: List[ChangeRecord] = field(default_factory=list)
    
    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.CRITICAL)
    
    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)
    
    @property
    def suggestion_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.SUGGESTION)
    
    @property
    def high_token_files(self) -> List[FileTokens]:
        """Return files with >1000 tokens."""
        return [f for f in self.file_tokens if f.tokens > 1000]


class Doctor:
    """Project doctor — diagnoses and fixes issues."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path.resolve()
        self.project_name = self.project_path.name
        self.venvs_dir = self.project_path.parent / "_venvs"
        self.artifacts_dir = self.project_path.parent / "_artifacts" / self.project_name
        self.data_dir = self.project_path.parent / "_data" / self.project_name
        self.archive_dir = self.project_path.parent / "_FOR_DELETION" / self.project_name
        self.issue_counter = 0
        self.changes: List[ChangeRecord] = []
    
    def _next_issue_id(self) -> int:
        self.issue_counter += 1
        return self.issue_counter
    
    def _count_tokens(self, path: Path) -> int:
        """Estimate token count for a path (file or directory)."""
        total = 0
        try:
            if path.is_file():
                content = path.read_text(encoding="utf-8", errors="ignore")
                total = len(content) // 4  # Rough estimate: 4 chars per token
            elif path.is_dir():
                for file in path.rglob("*"):
                    if file.is_file():
                        try:
                            content = file.read_text(encoding="utf-8", errors="ignore")
                            total += len(content) // 4
                        except Exception:
                            pass
        except Exception:
            pass
        return total
    
    def _get_dir_size(self, path: Path) -> int:
        """Get directory size in bytes."""
        total = 0
        try:
            for file in path.rglob("*"):
                if file.is_file():
                    total += file.stat().st_size
        except Exception:
            pass
        return total
    
    def _format_size(self, size_bytes: int) -> str:
        """Format bytes to human readable string."""
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f}TB"
    
    def _format_tokens(self, tokens: int) -> str:
        """Format token count to human readable string."""
        if tokens >= 1_000_000:
            return f"{tokens/1_000_000:.1f}M"
        elif tokens >= 1_000:
            return f"{tokens/1_000:.1f}K"
        return str(tokens)
    
    def diagnose(self, show_progress: bool = True) -> DiagnosticReport:
        """Run full project diagnosis."""
        issues = []
        total_tokens = 0
        file_tokens_list = []
        
        if show_progress:
            print(f"   [1/5] 📂 Scanning files...", end="", flush=True)
        
        # First, collect all files for progress tracking
        all_files = []
        for ext in ["*.py", "*.md", "*.txt", "*.json", "*.yaml", "*.yml", "*.toml"]:
            for file in self.project_path.rglob(ext):
                if not any(p in str(file) for p in ["venv", "node_modules", "__pycache__", ".git"]):
                    all_files.append(file)
        
        total_files = len(all_files)
        if show_progress:
            print(f" found {total_files} files")
            print(f"   [2/5] 🔢 Counting tokens...", end="", flush=True)
        
        # Calculate total tokens (only for relevant files)
        processed = 0
        for file in all_files:
            tokens = self._count_tokens(file)
            total_tokens += tokens
            processed += 1
            
            # Show progress every 50 files or at milestones
            if show_progress:
                if processed % 50 == 0 or processed == total_files:
                    pct = int(processed / total_files * 100) if total_files > 0 else 0
                    print(f"\r   [2/5] 🔢 Counting tokens... {pct}% ({processed}/{total_files})", end="", flush=True)
            
            # Track per-file tokens
            try:
                rel_path = file.relative_to(self.project_path)
                file_tokens_list.append(FileTokens(
                    path=file,
                    tokens=tokens,
                    relative_path=str(rel_path)
                ))
            except ValueError:
                pass
        
        if show_progress:
            print(f"\r   [2/5] 🔢 Counting tokens... done ({self._format_tokens(total_tokens)} total)")
            print(f"   [3/5] 🔍 Checking for issues...", end="", flush=True)
        
        # Sort by tokens (descending)
        file_tokens_list.sort(key=lambda x: x.tokens, reverse=True)
        
        # Check for venv inside project (recursive search - all levels)
        if show_progress:
            print(f"\r   [3/5] 🔍 Checking for issues... venvs", end="", flush=True)
        
        # Patterns to search for venv directories (recursively)
        # Exact names and patterns
        exact_names = ["venv", ".venv", "env", ".env"]
        pattern_prefixes = ["venv_", ".venv_"]
        found_venvs = set()  # Track found venvs to avoid duplicates
        
        # Search recursively for venv directories
        # First, search for exact names
        for name in exact_names:
            for venv_path in self.project_path.rglob(name):
                if venv_path.is_dir() and venv_path not in found_venvs:
                    # Verify it's actually a venv (has bin/Scripts or pyvenv.cfg)
                    is_venv = (
                        (venv_path / "bin").exists() or 
                        (venv_path / "Scripts").exists() or
                        (venv_path / "pyvenv.cfg").exists()
                    )
                    if is_venv:
                        found_venvs.add(venv_path)
                        tokens = self._count_tokens(venv_path)
                        size = self._get_dir_size(venv_path)
                        rel_path = venv_path.relative_to(self.project_path)
                        issues.append(Issue(
                            id=self._next_issue_id(),
                            severity=Severity.CRITICAL,
                            title=f"{rel_path}/ inside project",
                            description=f"Virtual environment consuming {self._format_tokens(tokens)} tokens ({self._format_size(size)})",
                            path=venv_path,
                            tokens_impact=tokens,
                            fix_function="fix_venv_inside"
                        ))
        
        # Then, search for pattern prefixes (venv_*, .venv_*)
        for prefix in pattern_prefixes:
            # Walk through all directories and check if name starts with prefix
            for root, dirs, _ in os.walk(self.project_path):
                root_path = Path(root)
                for dir_name in dirs:
                    if dir_name.startswith(prefix):
                        venv_path = root_path / dir_name
                        if venv_path not in found_venvs:
                            # Verify it's actually a venv
                            is_venv = (
                                (venv_path / "bin").exists() or 
                                (venv_path / "Scripts").exists() or
                                (venv_path / "pyvenv.cfg").exists()
                            )
                            if is_venv:
                                found_venvs.add(venv_path)
                                tokens = self._count_tokens(venv_path)
                                size = self._get_dir_size(venv_path)
                                rel_path = venv_path.relative_to(self.project_path)
                                issues.append(Issue(
                                    id=self._next_issue_id(),
                                    severity=Severity.CRITICAL,
                                    title=f"{rel_path}/ inside project",
                                    description=f"Virtual environment consuming {self._format_tokens(tokens)} tokens ({self._format_size(size)})",
                                    path=venv_path,
                                    tokens_impact=tokens,
                                    fix_function="fix_venv_inside"
                                ))
        
        # Check for __pycache__
        if show_progress:
            print(f"\r   [3/5] 🔍 Checking for issues... __pycache__", end="", flush=True)
        
        pycache_dirs = []
        try:
            for pycache in self.project_path.rglob("__pycache__"):
                if pycache.is_dir():
                    pycache_dirs.append(pycache)
        except Exception:
            pass  # Skip if there's an error
        
        if pycache_dirs:
            tokens = sum(self._count_tokens(p) for p in pycache_dirs)
            issues.append(Issue(
                id=self._next_issue_id(),
                severity=Severity.WARNING,
                title=f"__pycache__/ in {len(pycache_dirs)} locations",
                description=f"Python cache files consuming {self._format_tokens(tokens)} tokens",
                tokens_impact=tokens,
                fix_function="fix_pycache"
            ))
        
        # Check for logs directory (fast - single directory check)
        if show_progress:
            print(f"\r   [3/5] 🔍 Checking for issues... logs", end="", flush=True)
        
        logs_path = self.project_path / "logs"
        if logs_path.exists() and logs_path.is_dir():
            try:
                log_files = list(logs_path.rglob("*"))
                if log_files:
                    size = self._get_dir_size(logs_path)
                    tokens = self._count_tokens(logs_path)
                    issues.append(Issue(
                        id=self._next_issue_id(),
                        severity=Severity.WARNING,
                        title=f"logs/ folder ({len(log_files)} files)",
                        description=f"Log files consuming {self._format_tokens(tokens)} tokens ({self._format_size(size)})",
                        path=logs_path,
                        tokens_impact=tokens,
                        fix_function="fix_logs"
                    ))
            except Exception:
                pass  # Skip if there's an error
        
        # Check for .log files
        if show_progress:
            print(f"\r   [3/5] 🔍 Checking for issues... .log files", end="", flush=True)
        
        log_files = []
        try:
            for f in self.project_path.rglob("*.log"):
                if "venv" not in str(f) and f.is_file():
                    log_files.append(f)
        except Exception:
            pass
        
        if log_files:
            tokens = sum(self._count_tokens(f) for f in log_files)
            issues.append(Issue(
                id=self._next_issue_id(),
                severity=Severity.WARNING,
                title=f"{len(log_files)} .log files in project",
                description=f"Scattered log files consuming {self._format_tokens(tokens)} tokens",
                tokens_impact=tokens,
                fix_function="fix_log_files"
            ))
        
        # Check for node_modules (fast - single directory check)
        if show_progress:
            print(f"\r   [3/5] 🔍 Checking for issues... node_modules", end="", flush=True)
        
        node_modules = self.project_path / "node_modules"
        if node_modules.exists():
            size = self._get_dir_size(node_modules)
            issues.append(Issue(
                id=self._next_issue_id(),
                severity=Severity.CRITICAL,
                title="node_modules/ inside project",
                description=f"Node dependencies ({self._format_size(size)}) should be in .cursorignore",
                path=node_modules,
                tokens_impact=0,  # Usually ignored anyway
                fix_function="fix_node_modules"
            ))
        
        # Check for large data files
        if show_progress:
            print(f"\r   [3/5] 🔍 Checking for issues... large files", end="", flush=True)
        
        large_files = []
        try:
            # Check data file extensions
            for ext in ["*.csv", "*.db", "*.sqlite", "*.sqlite3", "*.jsonl", "*.json"]:
                for f in self.project_path.rglob(ext):
                    if f.is_file() and f.stat().st_size > 1_000_000:  # > 1MB
                        # Skip if it's in venv or node_modules
                        if "venv" not in str(f) and "node_modules" not in str(f):
                            # Skip protected files (e.g., package.json, pyproject.toml, etc.)
                            if is_protected_file(f):
                                continue
                            large_files.append(f)
        except Exception:
            pass
        
        if large_files:
            total_size = sum(f.stat().st_size for f in large_files)
            issues.append(Issue(
                id=self._next_issue_id(),
                severity=Severity.WARNING,
                title=f"{len(large_files)} large data files (>1MB)",
                description=f"Data files ({self._format_size(total_size)}) should be moved to ../_data/",
                tokens_impact=0,
                fix_function="fix_large_files"
            ))
        
        # Check for artifact files (FULL_PROJECT_CODE.txt, *_DUMP.txt, etc.)
        if show_progress:
            print(f"\r   [3/5] 🔍 Checking for issues... artifacts", end="", flush=True)
        
        artifact_files = []
        artifact_patterns = [
            "*FULL_PROJECT*.txt",
            "*_DUMP.txt",
            "*_CODE.txt",
            "*_BACKUP*.txt",
            "*_EXPORT*.txt",
            "*_ARCHIVE*.txt"
        ]
        
        try:
            for pattern in artifact_patterns:
                for f in self.project_path.rglob(pattern):
                    if f.is_file() and "venv" not in str(f):
                        # Skip protected files
                        if is_protected_file(f):
                            continue
                        artifact_files.append(f)
        except Exception:
            pass
        
        if artifact_files:
            total_size = sum(f.stat().st_size for f in artifact_files)
            total_tokens = sum(self._count_tokens(f) for f in artifact_files)
            issues.append(Issue(
                id=self._next_issue_id(),
                severity=Severity.CRITICAL,
                title=f"{len(artifact_files)} artifact files found",
                description=f"Artifact files ({self._format_size(total_size)}, {self._format_tokens(total_tokens)} tokens) should be moved to archive",
                tokens_impact=total_tokens,
                fix_function="fix_artifacts"
            ))
        
        # Check for large log/documentation files (.md files that are likely logs)
        if show_progress:
            print(f"\r   [3/5] 🔍 Checking for issues... large docs", end="", flush=True)
        
        large_doc_files = []
        try:
            for f in self.project_path.rglob("*.md"):
                if f.is_file() and "venv" not in str(f):
                    # Skip protected files
                    if is_protected_file(f):
                        continue
                    size = f.stat().st_size
                    # Check if it's a log file (large size + log-like name)
                    is_log = (
                        size > 100_000 or  # > 100KB
                        any(keyword in f.name.upper() for keyword in ["LOG", "HISTORY", "CHANGELOG", "PROJECT_LOG"])
                    )
                    if is_log and size > 50_000:  # > 50KB
                        large_doc_files.append(f)
        except Exception:
            pass
        
        if large_doc_files:
            total_size = sum(f.stat().st_size for f in large_doc_files)
            total_tokens = sum(self._count_tokens(f) for f in large_doc_files)
            issues.append(Issue(
                id=self._next_issue_id(),
                severity=Severity.WARNING,
                title=f"{len(large_doc_files)} large documentation/log files",
                description=f"Large .md files ({self._format_size(total_size)}, {self._format_tokens(total_tokens)} tokens) - consider archiving",
                tokens_impact=total_tokens,
                fix_function="fix_large_docs"
            ))
        
        # Check for high-token files that should be moved (smart recommendations)
        if show_progress:
            print(f"\r   [3/5] 🔍 Checking for issues... recommendations", end="", flush=True)
        
        # This will be populated after token counting, so we'll check it later
        
        # Check for missing _AI_INCLUDE (fast - single check)
        if show_progress:
            print(f"\r   [3/5] 🔍 Checking for issues... configs", end="", flush=True)
        
        # Check for missing _AI_INCLUDE
        ai_include = self.project_path / "_AI_INCLUDE"
        if not ai_include.exists():
            issues.append(Issue(
                id=self._next_issue_id(),
                severity=Severity.SUGGESTION,
                title="Missing _AI_INCLUDE/ folder",
                description="Project conventions and AI rules not defined",
                fix_function="fix_missing_ai_include"
            ))
        
        # Check for missing .cursorignore
        cursorignore = self.project_path / ".cursorignore"
        if not cursorignore.exists():
            issues.append(Issue(
                id=self._next_issue_id(),
                severity=Severity.SUGGESTION,
                title="Missing .cursorignore",
                description="Cursor will index everything including garbage",
                fix_function="fix_missing_cursorignore"
            ))
        
        # Check for missing bootstrap scripts
        bootstrap_sh = self.project_path / "scripts" / "bootstrap.sh"
        bootstrap_ps1 = self.project_path / "scripts" / "bootstrap.ps1"
        if not bootstrap_sh.exists() and not bootstrap_ps1.exists():
            issues.append(Issue(
                id=self._next_issue_id(),
                severity=Severity.SUGGESTION,
                title="Missing bootstrap scripts",
                description="No scripts/bootstrap.sh or bootstrap.ps1 for external venv",
                fix_function="fix_missing_bootstrap"
            ))
        
        if show_progress:
            print(f" found {len(issues)} issues so far")
            print(f"   [4/5] 🔎 Checking venvs & configs...", end="", flush=True)
        
        # Check for external venv
        external_venv = self.venvs_dir / f"{self.project_name}-main"
        external_venv_exists = external_venv.exists()
        
        if not external_venv_exists and not issues:
            # No venv anywhere
            issues.append(Issue(
                id=self._next_issue_id(),
                severity=Severity.SUGGESTION,
                title="No virtual environment found",
                description=f"Expected at {external_venv}",
                fix_function="fix_create_venv"
            ))
        
        if show_progress:
            print(f" done")
            print(f"   [5/5] 📊 Analyzing recommendations...", end="", flush=True)
            # Quick analysis summary
            critical = sum(1 for i in issues if i.severity == Severity.CRITICAL)
            warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
            suggestions = sum(1 for i in issues if i.severity == Severity.SUGGESTION)
            print(f" done")
            print(f"\n   ✅ Scan complete: {critical} critical, {warnings} warnings, {suggestions} suggestions\n")
        
        return DiagnosticReport(
            project_path=self.project_path,
            project_name=self.project_name,
            total_tokens=total_tokens,
            issues=issues,
            file_tokens=file_tokens_list,
            external_venv_exists=external_venv_exists,
            external_venv_path=external_venv if external_venv_exists else None,
            changes=self.changes
        )
    
    def create_backup(self) -> Path:
        """Create backup archive of the project (includes all files except venv, node_modules, __pycache__, .git)."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{self.project_name}_backup_{timestamp}.tar.gz"
        backup_path = self.project_path.parent / backup_name
        
        # Patterns to exclude from backup
        exclude_patterns = [
            "venv", ".venv", "venv_*", ".venv_*", "env", ".env",
            "node_modules", "__pycache__", ".git", ".pytest_cache",
            ".mypy_cache", ".ruff_cache", "*.pyc", "*.pyo"
        ]
        
        def should_exclude(path: Path) -> bool:
            """Check if path should be excluded from backup."""
            # Check if path matches any exclude pattern
            path_str = str(path.relative_to(self.project_path))
            path_parts = path_str.split(os.sep)
            
            # Check each part of the path
            for part in path_parts:
                # Exact matches
                if part in ["venv", ".venv", "env", ".env", "node_modules", "__pycache__", ".git", ".pytest_cache", ".mypy_cache", ".ruff_cache"]:
                    return True
                # Pattern matches (venv_*, .venv_*)
                if part.startswith("venv_") or part.startswith(".venv_"):
                    return True
                # File extensions
                if part.endswith((".pyc", ".pyo")):
                    return True
            return False
        
        # Use tarfile to create archive, recursively including all files
        with tarfile.open(backup_path, "w:gz") as tar:
            # Walk through all files and directories recursively
            for root, dirs, files in os.walk(self.project_path):
                root_path = Path(root)
                
                # Filter out excluded directories from os.walk
                dirs[:] = [d for d in dirs if not should_exclude(root_path / d)]
                
                # Add files
                for file in files:
                    file_path = root_path / file
                    if not should_exclude(file_path):
                        try:
                            arcname = file_path.relative_to(self.project_path)
                            tar.add(file_path, arcname=str(arcname), recursive=False)
                        except (OSError, PermissionError) as e:
                            # Skip files that can't be read (permissions, etc.)
                            continue
        
        return backup_path
    
    # === FIX FUNCTIONS ===
    
    def fix_venv_inside(self, issue: Issue) -> bool:
        """Move venv from inside project to external location (preserve libraries)."""
        if issue.path and issue.path.exists():
            # Calculate size before moving
            size = self._get_dir_size(issue.path)
            
            # Check if external venv already exists
            self.venvs_dir.mkdir(parents=True, exist_ok=True)
            external_venv = self.venvs_dir / f"{self.project_name}-main"
            
            if external_venv.exists():
                # External venv already exists - move old one to archive
                print(COLORS.info(f"   External venv already exists at {external_venv}"))
                print(COLORS.info(f"   Moving old venv to archive..."))
                
                self.archive_dir.mkdir(parents=True, exist_ok=True)
                venv_subdir = self.archive_dir / "venvs"
                venv_subdir.mkdir(exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_dest = venv_subdir / f"{issue.path.name}_{timestamp}"
                
                shutil.move(str(issue.path), str(archive_dest))
                
                # Record change
                self.changes.append(ChangeRecord(
                    action="moved",
                    item_type="venv",
                    source=issue.path,
                    destination=archive_dest,
                    size_bytes=size,
                    description=f"Moved {issue.path.name}/ to archive (external venv already exists)"
                ))
                
                print(COLORS.success(f"Moved {issue.path.name}/ to archive ({self._format_size(size)})"))
            else:
                # No external venv - move old one to correct location (preserve libraries!)
                print(COLORS.info(f"   Moving venv to external location (preserving libraries)..."))
                
                shutil.move(str(issue.path), str(external_venv))
                
                # Record change
                self.changes.append(ChangeRecord(
                    action="moved",
                    item_type="venv",
                    source=issue.path,
                    destination=external_venv,
                    size_bytes=size,
                    description=f"Moved {issue.path.name}/ to external location (libraries preserved)"
                ))
                
                print(COLORS.success(f"Moved {issue.path.name}/ to {external_venv} ({self._format_size(size)})"))
                print(COLORS.success("   ✅ All libraries preserved - no reinstallation needed!"))
            
            return True
        return False
    
    def fix_pycache(self, issue: Issue) -> bool:
        """Move all __pycache__ directories to archive."""
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        count = 0
        total_size = 0
        
        for pycache in self.project_path.rglob("__pycache__"):
            size = self._get_dir_size(pycache)
            total_size += size
            
            # Create archive path
            try:
                rel_path = pycache.relative_to(self.project_path)
                archive_name = str(rel_path).replace("/", "_").replace("\\", "_")
            except ValueError:
                archive_name = pycache.name
            
            archive_dest = self.archive_dir / f"pycache_{archive_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Move to archive
            shutil.move(str(pycache), str(archive_dest))
            count += 1
            
            # Record change
            self.changes.append(ChangeRecord(
                action="moved",
                item_type="cache",
                source=pycache,
                destination=archive_dest,
                size_bytes=size,
                description=f"Moved {rel_path if 'rel_path' in locals() else pycache.name} to archive"
            ))
        
        print(COLORS.success(f"Moved {count} __pycache__ directories to archive ({self._format_size(total_size)})"))
        return True
    
    def fix_logs(self, issue: Issue) -> bool:
        """Archive logs directory to external location."""
        if issue.path and issue.path.exists():
            # Create archive directory
            self.archive_dir.mkdir(parents=True, exist_ok=True)
            logs_subdir = self.archive_dir / "logs"
            logs_subdir.mkdir(exist_ok=True)
            
            # Calculate size before moving
            size = self._get_dir_size(issue.path)
            
            # Move entire logs directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_dest = logs_subdir / f"logs_directory_{timestamp}"
            
            shutil.move(str(issue.path), str(archive_dest))
            
            # Recreate empty logs dir
            issue.path.mkdir()
            (issue.path / ".gitkeep").touch()
            
            # Record change
            self.changes.append(ChangeRecord(
                action="moved",
                item_type="logs",
                source=issue.path,
                destination=archive_dest,
                size_bytes=size,
                description=f"Moved logs/ directory to archive"
            ))
            
            print(COLORS.success(f"Moved logs/ to archive ({self._format_size(size)})"))
            return True
        return False
    
    def fix_log_files(self, issue: Issue) -> bool:
        """Move scattered .log files to archive."""
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        logs_subdir = self.archive_dir / "logs"
        logs_subdir.mkdir(exist_ok=True)
        
        count = 0
        total_size = 0
        
        for log_file in self.project_path.rglob("*.log"):
            if "venv" not in str(log_file) and log_file.is_file():
                size = log_file.stat().st_size
                total_size += size
                
                # Move to archive
                archive_dest = logs_subdir / f"{log_file.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.move(str(log_file), str(archive_dest))
                count += 1
                
                # Record change
                try:
                    rel_path = log_file.relative_to(self.project_path)
                    self.changes.append(ChangeRecord(
                        action="moved",
                        item_type="logs",
                        source=log_file,
                        destination=archive_dest,
                        size_bytes=size,
                        description=f"Moved {rel_path} to archive"
                    ))
                except ValueError:
                    pass
        
        print(COLORS.success(f"Moved {count} .log files to archive ({self._format_size(total_size)})"))
        return True
    
    def fix_node_modules(self, issue: Issue) -> bool:
        """Add node_modules to .cursorignore (don't delete, just ignore)."""
        cursorignore = self.project_path / ".cursorignore"
        content = cursorignore.read_text() if cursorignore.exists() else ""
        
        if "node_modules" not in content:
            with open(cursorignore, "a") as f:
                f.write("\n# Node modules\nnode_modules/\n")
            print(COLORS.success("Added node_modules/ to .cursorignore"))
        return True
    
    def fix_large_files(self, issue: Issue) -> bool:
        """Move large data files to external location."""
        data_dest = self.data_dir
        data_dest.mkdir(parents=True, exist_ok=True)
        
        count = 0
        total_size = 0
        for ext in ["*.csv", "*.db", "*.sqlite", "*.sqlite3", "*.jsonl", "*.json"]:
            for f in self.project_path.rglob(ext):
                if f.is_file() and f.stat().st_size > 1_000_000:
                    if "venv" not in str(f) and "node_modules" not in str(f):
                        # Skip protected files - NEVER touch these!
                        if is_protected_file(f):
                            continue
                        size = f.stat().st_size
                        dest = data_dest / f.name
                        shutil.move(str(f), str(dest))
                        self.changes.append(ChangeRecord(
                            action="moved",
                            item_type="data_file",
                            source=f,
                            destination=dest,
                            size_bytes=size,
                            description=f"Moved large data file to ../_data/"
                        ))
                        count += 1
                        total_size += size
        
        if count > 0:
            print(COLORS.success(f"Moved {count} large files to {data_dest} ({self._format_size(total_size)})"))
        return count > 0
    
    def fix_artifacts(self, issue: Issue) -> bool:
        """Move artifact files (FULL_PROJECT_CODE.txt, etc.) to archive."""
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        artifacts_subdir = self.archive_dir / "artifacts"
        artifacts_subdir.mkdir(exist_ok=True)
        
        artifact_patterns = [
            "*FULL_PROJECT*.txt",
            "*_DUMP.txt",
            "*_CODE.txt",
            "*_BACKUP*.txt",
            "*_EXPORT*.txt",
            "*_ARCHIVE*.txt"
        ]
        
        count = 0
        total_size = 0
        
        for pattern in artifact_patterns:
            for f in self.project_path.rglob(pattern):
                if f.is_file() and "venv" not in str(f):
                    # Skip protected files - NEVER touch these!
                    if is_protected_file(f):
                        continue
                    size = f.stat().st_size
                    dest = artifacts_subdir / f.name
                    shutil.move(str(f), str(dest))
                    self.changes.append(ChangeRecord(
                        action="moved",
                        item_type="artifact",
                        source=f,
                        destination=dest,
                        size_bytes=size,
                        description=f"Moved artifact file to archive"
                    ))
                    count += 1
                    total_size += size
        
        if count > 0:
            print(COLORS.success(f"Moved {count} artifact files to archive ({self._format_size(total_size)})"))
        return count > 0
    
    def fix_large_docs(self, issue: Issue) -> bool:
        """Move large documentation/log files to archive."""
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        docs_subdir = self.archive_dir / "docs_logs"
        docs_subdir.mkdir(exist_ok=True)
        
        count = 0
        total_size = 0
        
        for f in self.project_path.rglob("*.md"):
            if f.is_file() and "venv" not in str(f):
                # Skip protected files - NEVER touch these!
                if is_protected_file(f):
                    continue
                size = f.stat().st_size
                # Check if it's a log file (large size + log-like name)
                is_log = (
                    size > 100_000 or  # > 100KB
                    any(keyword in f.name.upper() for keyword in ["LOG", "HISTORY", "CHANGELOG", "PROJECT_LOG"])
                )
                if is_log and size > 50_000:  # > 50KB
                    dest = docs_subdir / f.name
                    shutil.move(str(f), str(dest))
                    self.changes.append(ChangeRecord(
                        action="moved",
                        item_type="doc_log",
                        source=f,
                        destination=dest,
                        size_bytes=size,
                        description=f"Moved large documentation/log file to archive"
                    ))
                    count += 1
                    total_size += size
        
        if count > 0:
            print(COLORS.success(f"Moved {count} large doc/log files to archive ({self._format_size(total_size)})"))
        return count > 0
    
    def fix_missing_ai_include(self, issue: Issue) -> bool:
        """Create _AI_INCLUDE folder with basic files."""
        ai_include = self.project_path / "_AI_INCLUDE"
        ai_include.mkdir(exist_ok=True)
        
        # Create PROJECT_CONVENTIONS.md
        conventions = ai_include / "PROJECT_CONVENTIONS.md"
        conventions.write_text(f"""# Project Conventions — {self.project_name}

## Key Rules

1. **venv** — Always in `../_venvs/{self.project_name}-main/`
2. **Structure** — Follow existing patterns
3. **Logging** — Use `logging` module
4. **Config** — Use `config.py` and `.env`

## Code Style

- Python 3.10+
- Type hints required
- Docstrings on public functions
- Max 100 chars per line
""", encoding="utf-8")
        
        # Create WHERE_THINGS_LIVE.md
        where = ai_include / "WHERE_THINGS_LIVE.md"
        where.write_text(f"""# Where Things Live — {self.project_name}

## Source Code (read/edit freely)
- `src/**` or `handlers/**` — Main code
- `utils/**` — Utilities
- `api/**` — API routes
- `database/**` — DB operations

## External Locations
- `../_venvs/{self.project_name}-main` — Virtual environment
- `../_artifacts/{self.project_name}/logs` — Archived logs
- `../_data/{self.project_name}/` — Large data files

## Never Create Inside Project
- `venv/`, `.venv/`
- Large data files (>1MB)
- Log archives
""", encoding="utf-8")
        
        # Record changes
        self.changes.append(ChangeRecord(
            action="created",
            item_type="config",
            source=conventions,
            description="Created _AI_INCLUDE/PROJECT_CONVENTIONS.md"
        ))
        self.changes.append(ChangeRecord(
            action="created",
            item_type="config",
            source=where,
            description="Created _AI_INCLUDE/WHERE_THINGS_LIVE.md"
        ))
        
        print(COLORS.success("Created _AI_INCLUDE/ with conventions"))
        return True
    
    def fix_missing_cursorignore(self, issue: Issue) -> bool:
        """Create .cursorignore file."""
        cursorignore = self.project_path / ".cursorignore"
        cursorignore.write_text("""# Virtual environments
venv/
.venv/
**/site-packages/

# Python cache
**/__pycache__/
**/*.pyc
**/*.pyo

# Logs
logs/
*.log

# Data
**/*.csv
**/*.db
**/*.sqlite
**/*.sqlite3

# Node
node_modules/

# Git
.git/

# IDE
.idea/
.vscode/
""", encoding="utf-8")
        
        # Record change
        self.changes.append(ChangeRecord(
            action="created",
            item_type="config",
            source=cursorignore,
            description="Created .cursorignore"
        ))
        
        print(COLORS.success("Created .cursorignore"))
        return True
    
    def fix_missing_bootstrap(self, issue: Issue) -> bool:
        """Create bootstrap scripts."""
        scripts_dir = self.project_path / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        
        # bootstrap.sh
        bootstrap_sh = scripts_dir / "bootstrap.sh"
        bootstrap_sh.write_text(f"""#!/usr/bin/env bash
set -euo pipefail

PROJ="{self.project_name}"
VENV_DIR="../_venvs/${{PROJ}}-main"

mkdir -p "../_venvs"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating venv: $VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python -m pip install -U pip wheel setuptools --quiet

# Check if packages are already installed
if [ -f requirements.txt ]; then
    echo "Checking installed packages..."
    
    # Check if all requirements are satisfied
    if pip install -r requirements.txt --dry-run --quiet 2>&1 | grep -q "would install"; then
        echo "Installing missing packages..."
        pip install -r requirements.txt --quiet
    else
        echo "✅ All packages already installed"
    fi
fi

echo ""
echo "✅ Done! Activate: source $VENV_DIR/bin/activate"
""", encoding="utf-8")
        os.chmod(bootstrap_sh, 0o755)
        
        # bootstrap.ps1
        bootstrap_ps1 = scripts_dir / "bootstrap.ps1"
        ps1_content = f'''$PROJ = "{self.project_name}"
$VENV_DIR = "..\\_venvs\\$PROJ-main"

if (-not (Test-Path "..\\_venvs")) {{
    New-Item -ItemType Directory -Path "..\\_venvs" | Out-Null
}}

if (-not (Test-Path $VENV_DIR)) {{
    Write-Host "Creating venv: $VENV_DIR"
    python -m venv $VENV_DIR
}}

& "$VENV_DIR\\Scripts\\python.exe" -m pip install -U pip wheel setuptools --quiet

# Check if packages are already installed
if (Test-Path .\\requirements.txt) {{
    Write-Host "Checking installed packages..."
    
    # Check if all requirements are satisfied
    $dryRun = & "$VENV_DIR\\Scripts\\pip.exe" install -r requirements.txt --dry-run 2>&1
    if ($dryRun -match "would install") {{
        Write-Host "Installing missing packages..."
        & "$VENV_DIR\\Scripts\\pip.exe" install -r requirements.txt --quiet
    }} else {{
        Write-Host "✅ All packages already installed"
    }}
}}

Write-Host ""
Write-Host "✅ Done! Activate: $VENV_DIR\\Scripts\\Activate.ps1"
'''
        bootstrap_ps1.write_text(ps1_content, encoding="utf-8")
        
        # Record changes
        self.changes.append(ChangeRecord(
            action="created",
            item_type="script",
            source=bootstrap_sh,
            description="Created scripts/bootstrap.sh"
        ))
        self.changes.append(ChangeRecord(
            action="created",
            item_type="script",
            source=bootstrap_ps1,
            description="Created scripts/bootstrap.ps1"
        ))
        
        print(COLORS.success("Created scripts/bootstrap.sh and bootstrap.ps1"))
        return True
    
    def fix_create_venv(self, issue: Issue) -> bool:
        """Create external virtual environment."""
        self.venvs_dir.mkdir(parents=True, exist_ok=True)
        venv_path = self.venvs_dir / f"{self.project_name}-main"
        
        try:
            subprocess.run(
                ["python3", "-m", "venv", str(venv_path)],
                check=True,
                capture_output=True
            )
            print(COLORS.success(f"Created venv at {venv_path}"))
            return True
        except subprocess.CalledProcessError as e:
            print(COLORS.error(f"Failed to create venv: {e}"))
            return False
    
    def fix_issue(self, issue: Issue) -> bool:
        """Fix a single issue by calling its fix function."""
        if not issue.fix_function:
            return False
        
        fix_method = getattr(self, issue.fix_function, None)
        if fix_method:
            return fix_method(issue)
        return False
    
    def fix_all(self, report: DiagnosticReport, backup_path: Optional[Path] = None, auto: bool = False) -> bool:
        """Fix all issues in order of severity."""
        
        # === STEP 1: ARCHITECTURAL RESTRUCTURING (before any other fixes) ===
        # Check if project has "architectural obesity" (venv/data files inside root)
        has_architectural_issues = any(
            issue.severity == Severity.CRITICAL and 
            (issue.fix_function == "fix_venv_inside" or "venv" in issue.title.lower() or "data" in issue.title.lower())
            for issue in report.issues
        ) or any(
            "large data files" in issue.title.lower() or 
            "artifact" in issue.title.lower()
            for issue in report.issues
        )
        
        if has_architectural_issues and HAS_ARCHITECT:
            # Ask user in interactive mode
            if not auto:
                print("\n" + COLORS.warning("⚠️  Critical Architecture Issue: Project contains heavy venv/data files inside the root."))
                response = input("   Apply AI-Native restructuring (move to external folders)? [Y/n]: ").strip().upper()
                if response and response != "Y":
                    print(COLORS.info("   Skipping architectural restructuring."))
                    has_architectural_issues = False
            
            if has_architectural_issues:
                print(COLORS.info("\n🏗️  Running architectural restructuring..."))
                try:
                    # Run architectural restructuring
                    restructure_project(str(self.project_path))
                    
                    # CRITICAL: Verify config_paths.py exists (the bridge file)
                    config_paths_file = self.project_path / "config_paths.py"
                    if not config_paths_file.exists():
                        print(COLORS.warning("   ⚠️  config_paths.py not found after restructuring. Creating fallback..."))
                        # Create the bridge file as fallback
                        if create_config_paths:
                            create_config_paths(self.project_path, self.project_name)
                        else:
                            # Manual fallback creation
                            self._create_config_paths_fallback()
                    
                    # Verify it exists now
                    if config_paths_file.exists():
                        print(COLORS.success("   ✅ Bridge file (config_paths.py) verified."))
                    else:
                        print(COLORS.error("   ❌ Failed to create config_paths.py. Project may not function correctly."))
                    
                    # Record architectural restructuring in changes
                    self.changes.append(ChangeRecord(
                        action="restructured",
                        item_type="architecture",
                        source=self.project_path,
                        destination=None,
                        size_bytes=0,
                        description="Applied AI-Native architectural restructuring (venv/data moved external)"
                    ))
                    
                except Exception as e:
                    print(COLORS.error(f"   ❌ Architectural restructuring failed: {e}"))
                    print(COLORS.warning("   Continuing with standard fixes..."))
        
        # === STEP 2: STANDARD FIXES (after architectural restructuring) ===
        # Sort: CRITICAL first, then WARNING, then SUGGESTION
        sorted_issues = sorted(
            report.issues,
            key=lambda x: (
                0 if x.severity == Severity.CRITICAL else
                1 if x.severity == Severity.WARNING else 2
            )
        )
        
        success_count = 0
        for issue in sorted_issues:
            # Skip issues that were already handled by architectural restructuring
            if has_architectural_issues and HAS_ARCHITECT:
                if issue.fix_function in ["fix_venv_inside", "fix_large_files"]:
                    # These were handled by architect, but we still want to check if they need additional fixes
                    # Skip only if architect successfully handled them
                    continue
            
            print(f"\n   [{issue.id}] Fixing: {issue.title}")
            if self.fix_issue(issue):
                success_count += 1
            else:
                print(COLORS.warning(f"Could not fix: {issue.title}"))
        
        # Run bootstrap if venv was deleted
        venv_deleted = any(
            i.fix_function == "fix_venv_inside" 
            for i in sorted_issues 
            if i.severity == Severity.CRITICAL
        )
        
        if venv_deleted:
            print("\n   Running bootstrap to create external venv...")
            bootstrap = self.project_path / "scripts" / "bootstrap.sh"
            if not bootstrap.exists():
                self.fix_missing_bootstrap(Issue(0, Severity.SUGGESTION, "", ""))
            
            # Try to run bootstrap
            try:
                if os.name == "nt":  # Windows
                    subprocess.run(
                        ["powershell", "-File", str(self.project_path / "scripts" / "bootstrap.ps1")],
                        cwd=self.project_path,
                        check=True
                    )
                else:
                    subprocess.run(
                        ["bash", str(bootstrap)],
                        cwd=self.project_path,
                        check=True
                    )
                print(COLORS.success("External venv created"))
            except subprocess.CalledProcessError:
                print(COLORS.warning("Bootstrap failed — run manually: ./scripts/bootstrap.sh"))
        
        return success_count == len(sorted_issues)
    
    def _create_config_paths_fallback(self) -> None:
        """Fallback method to create config_paths.py if architect module is not available."""
        config_content = f'''import os
from pathlib import Path

# === AI-NATIVE PATH CONFIGURATION ===
# Auto-generated by AI Toolkit Doctor

BASE_DIR = Path(__file__).resolve().parent
PROJECT_NAME = "{self.project_name}"
EXTERNAL_ROOT = BASE_DIR.parent

# 1. DATA (JSON, DB, CSV)
DATA_DIR = EXTERNAL_ROOT / "_data" / PROJECT_NAME
if not DATA_DIR.exists():
    DATA_DIR = BASE_DIR / "data"

# 2. LOGS
LOGS_DIR = EXTERNAL_ROOT / "_logs" / PROJECT_NAME
if not LOGS_DIR.exists():
    LOGS_DIR = BASE_DIR / "logs"

# 3. VENV (Reference only)
VENV_DIR = EXTERNAL_ROOT / "_venvs" / PROJECT_NAME

def get_path(filename, check_exists=False):
    """Smart path resolver: External > Internal"""
    external_path = DATA_DIR / filename
    local_path = BASE_DIR / filename
    
    if check_exists:
        if external_path.exists(): return external_path
        if local_path.exists(): return local_path
    
    return external_path
'''
        config_path = self.project_path / "config_paths.py"
        try:
            config_path.write_text(config_content, encoding="utf-8")
            print(COLORS.success(f"   ✅ Created fallback config_paths.py"))
        except Exception as e:
            print(COLORS.error(f"   ❌ Failed to create config_paths.py: {e}"))


def _update_project_docs(project_path: Path) -> None:
    """
    Update both PROJECT_STATUS.md and CURRENT_CONTEXT_MAP.md after changes.
    
    IMPORTANT: Only updates docs if this is the AI Toolkit project itself,
    not when running doctor on other projects!
    """
    # Check if this is the AI Toolkit project (has status_generator.py)
    status_gen = project_path / "src" / "utils" / "status_generator.py"
    if not status_gen.exists():
        # This is not AI Toolkit, skip doc updates
        return
    
    try:
        # Update PROJECT_STATUS.md
        update_status(project_path, skip_tests=True)
        print(COLORS.success("✅ PROJECT_STATUS.md updated"))
        
        # Update CURRENT_CONTEXT_MAP.md
        if HAS_CONTEXT_MAP and write_context_map:
            try:
                if write_context_map(project_path, "CURRENT_CONTEXT_MAP.md"):
                    print(COLORS.success("✅ CURRENT_CONTEXT_MAP.md updated"))
                else:
                    print(COLORS.warning("⚠️  Could not update CURRENT_CONTEXT_MAP.md"))
            except Exception as e:
                print(COLORS.warning(f"⚠️  Could not update CURRENT_CONTEXT_MAP.md: {e}"))
        else:
            # Fallback: try to run generate_map.py script
            try:
                import subprocess
                generate_map_script = project_path / "generate_map.py"
                if generate_map_script.exists():
                    result = subprocess.run(
                        ["python3", str(generate_map_script)],
                        cwd=project_path,
                        check=False,
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        print(COLORS.success("✅ CURRENT_CONTEXT_MAP.md updated (via script)"))
                    else:
                        print(COLORS.warning("⚠️  Could not update CURRENT_CONTEXT_MAP.md (script failed)"))
                else:
                    print(COLORS.warning("⚠️  generate_map.py not found, skipping CURRENT_CONTEXT_MAP.md update"))
            except Exception as e:
                print(COLORS.warning(f"⚠️  Could not update CURRENT_CONTEXT_MAP.md: {e}"))
    except Exception as e:
        print(COLORS.error(f"❌ Error updating project docs: {e}"))


def print_report(report: DiagnosticReport, show_menu: bool = True) -> None:
    """Print formatted diagnostic report."""
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  🏥 AI TOOLKIT DOCTOR — Project Analysis                         ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    
    # Project info
    project_display = report.project_name[:50]
    print(f"║  Project: {project_display:<55} ║")
    
    path_display = str(report.project_path)[:50]
    print(f"║  Path:    {path_display:<55} ║")
    
    # Token status
    if report.total_tokens > 1_000_000:
        token_str = f"{report.total_tokens/1_000_000:.1f}M tokens (CRITICAL)"
    elif report.total_tokens > 100_000:
        token_str = f"{report.total_tokens/1_000:.0f}K tokens (HIGH)"
    else:
        token_str = f"{report.total_tokens/1_000:.0f}K tokens (OK)"
    
    print(f"║  Tokens:  {token_str:<55} ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    
    # Issues by severity
    critical = [i for i in report.issues if i.severity == Severity.CRITICAL]
    warnings = [i for i in report.issues if i.severity == Severity.WARNING]
    suggestions = [i for i in report.issues if i.severity == Severity.SUGGESTION]
    
    if critical:
        print(f"║  🔴 CRITICAL ISSUES ({len(critical)})                                         ║")
        for issue in critical:
            line = f"  ├─ [{issue.id}] {issue.title}"[:60]
            print(f"║{line:<67}║")
    
    if warnings:
        print(f"║  🟡 WARNINGS ({len(warnings)})                                                ║")
        for issue in warnings:
            line = f"  ├─ [{issue.id}] {issue.title}"[:60]
            print(f"║{line:<67}║")
    
    if suggestions:
        print(f"║  🟢 SUGGESTIONS ({len(suggestions)})                                            ║")
        for issue in suggestions:
            line = f"  ├─ [{issue.id}] {issue.title}"[:60]
            print(f"║{line:<67}║")
    
    if not report.issues:
        print("║  ✅ No issues found! Project is healthy.                         ║")
    
    print("╠══════════════════════════════════════════════════════════════════╣")
    
    # Show token breakdown for high-token files
    high_token_files = report.high_token_files[:10]  # Top 10
    if high_token_files:
        print("║  📊 TOP TOKEN CONSUMERS (>1K tokens)                             ║")
        for ft in high_token_files[:5]:  # Show top 5 in main report
            # Truncate path if too long
            path_display = ft.relative_path
            if len(path_display) > 45:
                path_display = "..." + path_display[-42:]
            
            tokens_display = f"{ft.tokens/1000:.1f}K"
            line = f"  • {path_display} — {tokens_display}"[:65]
            print(f"║{line:<67}║")
        
        if len(high_token_files) > 5:
            remaining = len(high_token_files) - 5
            print(f"║  ... and {remaining} more files >1K tokens                                ║")
    
    # Always print the closing box line
    if show_menu:
        print("╠══════════════════════════════════════════════════════════════════╣")
        
        if report.issues:
            print("║  ACTIONS:                                                        ║")
            print("║  [1-9] Fix specific issue    [A] Fix ALL    [R] Report    [Q] Quit║")
            print("║  [T] Show full token breakdown                                   ║")
        else:
            print("║  [R] Generate report    [T] Token breakdown    [Q] Quit          ║")
    
    # Always print closing line (even if menu is hidden)
    print("╚══════════════════════════════════════════════════════════════════╝")


def print_token_breakdown(report: DiagnosticReport) -> None:
    """Print detailed token breakdown."""
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  📊 DETAILED TOKEN BREAKDOWN                                     ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print(f"║  Total: {report.total_tokens/1000:.1f}K tokens across {len(report.file_tokens)} files                     ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    
    # Show all files >1000 tokens
    high_token_files = report.high_token_files
    if high_token_files:
        print("║  FILES WITH >1000 TOKENS:                                        ║")
        print("║                                                                  ║")
        
        for ft in high_token_files[:20]:  # Top 20
            path_display = ft.relative_path
            if len(path_display) > 45:
                path_display = "..." + path_display[-42:]
            
            tokens_display = f"{ft.tokens:,}".rjust(7)
            line = f"  {tokens_display} — {path_display}"[:65]
            print(f"║{line:<67}║")
        
        if len(high_token_files) > 20:
            remaining = len(high_token_files) - 20
            print(f"║  ... and {remaining} more files                                          ║")
    
    # Show summary by file type
    print("╠══════════════════════════════════════════════════════════════════╣")
    print("║  BREAKDOWN BY FILE TYPE:                                         ║")
    print("║                                                                  ║")
    
    by_ext = {}
    for ft in report.file_tokens:
        ext = ft.path.suffix or "(no ext)"
        if ext not in by_ext:
            by_ext[ext] = {"count": 0, "tokens": 0}
        by_ext[ext]["count"] += 1
        by_ext[ext]["tokens"] += ft.tokens
    
    # Sort by tokens
    sorted_ext = sorted(by_ext.items(), key=lambda x: x[1]["tokens"], reverse=True)
    
    for ext, data in sorted_ext[:10]:
        tokens_display = f"{data['tokens']/1000:.1f}K".rjust(8)
        count_display = f"({data['count']} files)"
        line = f"  {ext.ljust(10)} {tokens_display} {count_display}"[:65]
        print(f"║{line:<67}║")
    
    print("╚══════════════════════════════════════════════════════════════════╝")


def print_detailed_changes(report: DiagnosticReport) -> None:
    """Print detailed list of all changes made."""
    if not report.changes:
        return
    
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  📋 DETAILED CHANGE REPORT                                       ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    
    # Group by action
    by_action = {}
    total_size = 0
    
    for change in report.changes:
        if change.action not in by_action:
            by_action[change.action] = []
        by_action[change.action].append(change)
        total_size += change.size_bytes
    
    # Show by action type
    action_icons = {
        "moved": "📦",
        "archived": "📚",
        "created": "✨"
    }
    
    for action in ["moved", "archived", "created"]:
        if action in by_action:
            changes_list = by_action[action]
            icon = action_icons.get(action, "•")
            print(f"║  {icon} {action.upper()} ({len(changes_list)} items)                                    ║")
            print("║                                                                  ║")
            
            for change in changes_list:
                # Format source path
                if change.source:
                    try:
                        src_display = str(change.source.relative_to(report.project_path))
                        if len(src_display) > 35:
                            src_display = "..." + src_display[-32:]
                    except ValueError:
                        src_display = str(change.source.name)
                else:
                    src_display = change.description
                
                # Format destination if exists
                if change.destination:
                    try:
                        dst_display = str(change.destination.relative_to(report.project_path.parent))
                        if len(dst_display) > 30:
                            dst_display = "..." + dst_display[-27:]
                    except ValueError:
                        dst_display = str(change.destination.name)
                    
                    # Format size
                    size_str = ""
                    if change.size_bytes > 0:
                        if change.size_bytes >= 1_000_000_000:
                            size_str = f" ({change.size_bytes/1_000_000_000:.2f} GB)"
                        elif change.size_bytes >= 1_000_000:
                            size_str = f" ({change.size_bytes/1_000_000:.2f} MB)"
                        elif change.size_bytes >= 1_000:
                            size_str = f" ({change.size_bytes/1_000:.2f} KB)"
                    
                    line = f"    {src_display:<35} → {dst_display}{size_str}"[:65]
                else:
                    line = f"    {src_display}"[:65]
                
                print(f"║{line:<67}║")
            
            print("║                                                                  ║")
    
    # Summary
    print("╠══════════════════════════════════════════════════════════════════╣")
    print(f"║  📊 SUMMARY:                                                      ║")
    print(f"║     Total changes: {len(report.changes)}                                              ║")
    
    if total_size > 0:
        # Format total size
        if total_size >= 1_000_000_000:
            total_str = f"{total_size/1_000_000_000:.2f} GB"
        elif total_size >= 1_000_000:
            total_str = f"{total_size/1_000_000:.2f} MB"
        elif total_size >= 1_000:
            total_str = f"{total_size/1_000:.2f} KB"
        else:
            total_str = f"{total_size} B"
        
        print(f"║     Space moved: {total_str:<50} ║")
    
    # Show archive location
    archive_path = report.project_path.parent / "_FOR_DELETION" / report.project_name
    print(f"║     Archive location: {str(archive_path.relative_to(report.project_path.parent))[:45]:<45} ║")
    print(f"║     ⚠️  Review and delete manually when safe                        ║")
    
    print("╚══════════════════════════════════════════════════════════════════╝")


def print_result(before: DiagnosticReport, after: DiagnosticReport, backup_path: Optional[Path] = None) -> None:
    """Print before/after comparison."""
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  ✅ DOCTOR COMPLETE — All issues processed!                      ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print("║                      BEFORE           AFTER                      ║")
    
    # Token reduction
    before_tokens = f"{before.total_tokens/1_000:.0f}K" if before.total_tokens < 1_000_000 else f"{before.total_tokens/1_000_000:.1f}M"
    after_tokens = f"{after.total_tokens/1_000:.0f}K" if after.total_tokens < 1_000_000 else f"{after.total_tokens/1_000_000:.1f}M"
    
    if before.total_tokens > 0:
        reduction = int((1 - after.total_tokens / before.total_tokens) * 100)
        reduction_str = f"({reduction}% reduction)" if reduction > 0 else "(no change)"
    else:
        reduction_str = ""
    
    print(f"║  Tokens:       {before_tokens:>10}    →    {after_tokens:<10} {reduction_str:<15}║")
    print(f"║  Critical:     {before.critical_count:>10}    →    {after.critical_count:<10}                 ║")
    print(f"║  Warnings:     {before.warning_count:>10}    →    {after.warning_count:<10}                 ║")
    
    print("╠══════════════════════════════════════════════════════════════════╣")
    
    if backup_path:
        backup_name = backup_path.name[:50]
        print(f"║  📦 Backup: {backup_name:<53}║")
    
    if after.external_venv_exists:
        venv_display = str(after.external_venv_path)[:50]
        print(f"║  🌐 Venv: {venv_display:<55}║")
    
    print("║                                                                  ║")
    print("║  Your project is now AI-ready! 🚀                                ║")
    print("╚══════════════════════════════════════════════════════════════════╝")


def run_doctor(project_path: Path, auto: bool = False, report_only: bool = False) -> bool:
    """
    Main doctor flow.
    
    Args:
        project_path: Path to project
        auto: If True, fix everything without asking
        report_only: If True, only show report, don't offer fixes
    """
    doctor = Doctor(project_path)
    
    print(COLORS.info(f"\nDiagnosing project: {doctor.project_name}"))
    print(COLORS.info(f"   Path: {project_path}\n"))
    
    # Run diagnosis
    report = doctor.diagnose()
    
    # Always show menu unless in report-only mode
    show_menu_flag = not report_only
    print_report(report, show_menu=show_menu_flag)
    
    # Force flush to ensure menu is visible
    import sys
    sys.stdout.flush()
    sys.stderr.flush()
    
    if report_only:
        # In report-only mode, just exit after showing report
        return True
    
    if not report.issues:
        # Update both docs and exit
        _update_project_docs(project_path)
        return True
    
    if auto:
        # Auto-fix everything
        print(COLORS.info("\nAuto-fix mode — fixing all issues..."))
        print(COLORS.info("   Creating backup first..."))
        backup_path = doctor.create_backup()
        print(COLORS.success(f"Backup: {backup_path.name}"))
        
        doctor.fix_all(report, backup_path, auto=True)
        
        # Re-diagnose to get updated report with changes
        after = doctor.diagnose()
        after.changes = doctor.changes  # Transfer changes from doctor instance
        
        print_result(report, after, backup_path)
        
        # Show detailed changes
        print_detailed_changes(after)
        
        # Update both PROJECT_STATUS.md and CURRENT_CONTEXT_MAP.md
        _update_project_docs(project_path)
        
        return True
    
    # Interactive mode
    import sys
    
    print()  # Extra newline for clarity
    sys.stdout.flush()  # Ensure all output is flushed before waiting for input
    
    while True:
        try:
            # Explicitly flush before input to ensure prompt is visible
            sys.stdout.flush()
            sys.stderr.flush()
            choice = input("> Enter choice: ").strip().upper()
            
            # If we get an empty string, it might mean stdin was closed
            if not choice and not sys.stdin.isatty():
                print(COLORS.warning("\n⚠️  Input not available. Use --auto or --report mode instead."))
                break
                
        except (KeyboardInterrupt, EOFError) as e:
            # If EOFError happens, it means stdin isn't available
            # This can happen in non-interactive environments
            print(COLORS.warning("\n⚠️  Cannot read input. Use --auto or --report mode instead."))
            break
        except Exception as e:
            # Catch any other unexpected errors
            print(COLORS.error(f"\n❌ Error reading input: {e}"))
            print(COLORS.info("Try using --auto or --report mode instead."))
            break
        
        if choice == "Q":
            break
        elif choice == "T":
            # Show token breakdown
            print_token_breakdown(report)
        elif choice == "R":
            # Just update docs
            _update_project_docs(project_path)
        elif choice == "A":
            # Fix all
            print(COLORS.info("\nFixing all issues..."))
            print(COLORS.info("   Creating backup first..."))
            backup_path = doctor.create_backup()
            print(COLORS.success(f"Backup: {backup_path.name}"))
            
            doctor.fix_all(report, backup_path, auto=False)
            
            # Re-diagnose to get updated report with changes
            after = doctor.diagnose()
            after.changes = doctor.changes  # Transfer changes from doctor instance
            
            print_result(report, after, backup_path)
            
            # Show detailed changes
            print_detailed_changes(after)
            
            # Update both docs
            _update_project_docs(project_path)
            break
        elif choice.isdigit():
            issue_id = int(choice)
            issue = next((i for i in report.issues if i.id == issue_id), None)
            if issue:
                print(f"\n   Fixing: {issue.title}")
                doctor.fix_issue(issue)
                
                # Re-diagnose and show updated report
                report = doctor.diagnose()
                print_report(report)
            else:
                print(COLORS.warning(f"Issue {issue_id} not found"))
        else:
            print(COLORS.warning("Invalid choice"))
    
    return True


def cmd_doctor(args=None) -> bool:
    """CLI entry point for doctor command."""
    # Get project path
    if args and hasattr(args, 'path') and args.path:
        project_path = Path(args.path).resolve()
    else:
        project_path = Path.cwd()
    
    if not project_path.exists():
        print(COLORS.error(f"Path not found: {project_path}"))
        return False
    
    # Check flags
    auto = args and hasattr(args, 'auto') and args.auto
    report_only = args and hasattr(args, 'report') and args.report
    
    return run_doctor(project_path, auto=auto, report_only=report_only)


def run_doctor_interactive() -> None:
    """Interactive doctor command for menu."""
    print(COLORS.colorize("\n🏥 PROJECT DOCTOR\n", COLORS.GREEN))
    
    path_str = input("Project path (Enter = current folder): ").strip()
    if not path_str:
        path_str = "."
    
    project_path = Path(path_str).resolve()
    if not project_path.exists():
        print(COLORS.error(f"Path does not exist: {project_path}"))
        return
    
    mode = input("Mode: [1] Interactive  [2] Auto-fix  [3] Report only: ").strip()
    
    class Args:
        pass
    
    args = Args()
    args.path = project_path
    args.auto = mode == "2"
    args.report = mode == "3"
    
    cmd_doctor(args)

