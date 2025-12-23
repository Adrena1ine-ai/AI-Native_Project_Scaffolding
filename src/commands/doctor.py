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
        
        # Check for venv inside project (fast - only root level)
        if show_progress:
            print(f"\r   [3/5] 🔍 Checking for issues... venvs", end="", flush=True)
        
        for venv_name in ["venv", ".venv", "venv_gate", ".venv_parser", "env", ".env"]:
            venv_path = self.project_path / venv_name
            if venv_path.exists() and venv_path.is_dir():
                # Verify it's actually a venv (has bin/Scripts or pyvenv.cfg)
                is_venv = (
                    (venv_path / "bin").exists() or 
                    (venv_path / "Scripts").exists() or
                    (venv_path / "pyvenv.cfg").exists()
                )
                if is_venv:
                    tokens = self._count_tokens(venv_path)
                    size = self._get_dir_size(venv_path)
                    issues.append(Issue(
                        id=self._next_issue_id(),
                        severity=Severity.CRITICAL,
                        title=f"{venv_name}/ inside project",
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
            for ext in ["*.csv", "*.db", "*.sqlite", "*.sqlite3", "*.jsonl"]:
                for f in self.project_path.rglob(ext):
                    if f.is_file() and f.stat().st_size > 1_000_000:  # > 1MB
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
        """Create backup archive of the project."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{self.project_name}_backup_{timestamp}.tar.gz"
        backup_path = self.project_path.parent / backup_name
        
        # Use tarfile to create archive, excluding venv
        with tarfile.open(backup_path, "w:gz") as tar:
            for item in self.project_path.iterdir():
                if item.name not in ["venv", ".venv", "venv_gate", "node_modules", "__pycache__", ".git"]:
                    tar.add(item, arcname=item.name)
        
        return backup_path
    
    # === FIX FUNCTIONS ===
    
    def fix_venv_inside(self, issue: Issue) -> bool:
        """Delete venv inside project and create external one."""
        if issue.path and issue.path.exists():
            shutil.rmtree(issue.path)
            print(COLORS.success(f"Deleted {issue.path.name}/"))
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
        for ext in ["*.csv", "*.db", "*.sqlite", "*.sqlite3", "*.jsonl"]:
            for f in self.project_path.rglob(ext):
                if f.is_file() and f.stat().st_size > 1_000_000:
                    dest = data_dest / f.name
                    shutil.move(str(f), str(dest))
                    count += 1
        
        print(COLORS.success(f"Moved {count} large files to {data_dest}"))
        return True
    
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
    
    def fix_all(self, report: DiagnosticReport, backup_path: Optional[Path] = None) -> bool:
        """Fix all issues in order of severity."""
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
    
    if show_menu:
        print("╠══════════════════════════════════════════════════════════════════╣")
        
        if report.issues:
            print("║  ACTIONS:                                                        ║")
            print("║  [1-9] Fix specific issue    [A] Fix ALL    [R] Report    [Q] Quit║")
            print("║  [T] Show full token breakdown                                   ║")
        else:
            print("║  [R] Generate report    [T] Token breakdown    [Q] Quit          ║")
    
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
    print_report(report, show_menu=not report_only)
    
    if report_only:
        # In report-only mode, just exit after showing report
        return True
    
    if not report.issues:
        # Update status and exit
        update_status(project_path, skip_tests=True)
        print(COLORS.success("\nPROJECT_STATUS.md updated"))
        return True
    
    if auto:
        # Auto-fix everything
        print(COLORS.info("\nAuto-fix mode — fixing all issues..."))
        print(COLORS.info("   Creating backup first..."))
        backup_path = doctor.create_backup()
        print(COLORS.success(f"Backup: {backup_path.name}"))
        
        doctor.fix_all(report, backup_path)
        
        # Re-diagnose to get updated report with changes
        after = doctor.diagnose()
        after.changes = doctor.changes  # Transfer changes from doctor instance
        
        print_result(report, after, backup_path)
        
        # Show detailed changes
        print_detailed_changes(after)
        
        # Update status
        update_status(project_path, skip_tests=True)
        print(COLORS.success("\nPROJECT_STATUS.md updated"))
        
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
            # Just update status
            update_status(project_path, skip_tests=True)
            print(COLORS.success("PROJECT_STATUS.md updated"))
        elif choice == "A":
            # Fix all
            print(COLORS.info("\nFixing all issues..."))
            print(COLORS.info("   Creating backup first..."))
            backup_path = doctor.create_backup()
            print(COLORS.success(f"Backup: {backup_path.name}"))
            
            doctor.fix_all(report, backup_path)
            
            # Re-diagnose to get updated report with changes
            after = doctor.diagnose()
            after.changes = doctor.changes  # Transfer changes from doctor instance
            
            print_result(report, after, backup_path)
            
            # Show detailed changes
            print_detailed_changes(after)
            
            # Update status
            update_status(project_path, skip_tests=True)
            print(COLORS.success("\nPROJECT_STATUS.md updated"))
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

