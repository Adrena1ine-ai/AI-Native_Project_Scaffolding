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
    is_movable: bool = False
    move_reason: str = ""


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
        self.issue_counter = 0
    
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
    
    def _analyze_file_movability(self, file_path: Path, rel_path: str, tokens: int) -> tuple[bool, str]:
        """
        Analyze if a file can be safely moved to _AI_ARCHIVE.
        
        Returns:
            (is_movable, reason)
        """
        name_lower = file_path.name.lower()
        path_lower = str(rel_path).lower()
        
        # Patterns indicating movable files
        movable_patterns = [
            # Historical/archived code
            (["old", "legacy", "deprecated", "archive", "backup", "bak"], "Historical/archived file"),
            (["example", "sample", "demo", "test_data"], "Example/sample file"),
            (["_old", "_backup", "_archive", ".old", ".bak"], "Backup file"),
            
            # Documentation that's not essential
            (["changelog", "history", "migration", "upgrade"], "Historical documentation"),
            (["screenshot", "image", "diagram"], "Media file"),
            
            # Libraries/dependencies (if copied into project)
            (["lib/", "libs/", "vendor/", "third_party/", "external/"], "External library"),
            
            # Generated files
            (["generated", "auto_generated", ".generated"], "Generated file"),
            
            # Large documentation
            (["api_docs", "reference", "spec/"], "Reference documentation"),
        ]
        
        # Check if file matches movable patterns
        for patterns, reason in movable_patterns:
            for pattern in patterns:
                if pattern in name_lower or pattern in path_lower:
                    return True, reason
        
        # Large markdown files might be documentation
        if file_path.suffix == ".md" and tokens > 3000:
            # But not if it's README, CONTRIBUTING, etc.
            essential_docs = ["readme", "contributing", "license", "changelog", "quickstart"]
            if not any(doc in name_lower for doc in essential_docs):
                return True, "Large documentation (>3K tokens)"
        
        # Very large Python files might be generated or libraries
        if file_path.suffix == ".py" and tokens > 10000:
            # Check if it looks like generated code
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                lines = content.split("\n")
                
                # Count comment density
                comment_lines = sum(1 for line in lines if line.strip().startswith("#"))
                if len(lines) > 0 and (comment_lines / len(lines)) > 0.3:
                    return True, "Likely generated code (high comment density)"
                
                # Check for auto-generated markers
                first_50_lines = "\n".join(lines[:50])
                if any(marker in first_50_lines.lower() for marker in [
                    "auto-generated", "autogenerated", "do not edit", 
                    "generated by", "code generator"
                ]):
                    return True, "Auto-generated code"
            except Exception:
                pass
        
        return False, ""
    
    def diagnose(self) -> DiagnosticReport:
        """Run full project diagnosis."""
        issues = []
        total_tokens = 0
        file_tokens_list = []
        
        # Calculate total tokens (only for relevant files)
        for ext in ["*.py", "*.md", "*.txt", "*.json", "*.yaml", "*.yml", "*.toml"]:
            for file in self.project_path.rglob(ext):
                if not any(p in str(file) for p in ["venv", "node_modules", "__pycache__", ".git"]):
                    tokens = self._count_tokens(file)
                    total_tokens += tokens
                    
                    # Track per-file tokens and analyze movability
                    try:
                        rel_path = file.relative_to(self.project_path)
                        is_movable, move_reason = self._analyze_file_movability(file, str(rel_path), tokens)
                        
                        file_tokens_list.append(FileTokens(
                            path=file,
                            tokens=tokens,
                            relative_path=str(rel_path),
                            is_movable=is_movable,
                            move_reason=move_reason
                        ))
                    except ValueError:
                        pass
        
        # Sort by tokens (descending)
        file_tokens_list.sort(key=lambda x: x.tokens, reverse=True)
        
        # Check for venv inside project (recursively search all subdirectories)
        venv_patterns = ["venv", ".venv", "venv_*", ".venv_*", "env", ".env"]
        found_venvs = []
        
        for pattern in venv_patterns:
            for venv_path in self.project_path.rglob(pattern):
                if venv_path.is_dir() and venv_path not in found_venvs:
                    # Verify it's actually a venv (has bin/Scripts or pyvenv.cfg)
                    is_venv = (
                        (venv_path / "bin").exists() or 
                        (venv_path / "Scripts").exists() or
                        (venv_path / "pyvenv.cfg").exists()
                    )
                    if is_venv:
                        found_venvs.append(venv_path)
                        tokens = self._count_tokens(venv_path)
                        size = self._get_dir_size(venv_path)
                        
                        # Show relative path from project root
                        try:
                            rel_path = venv_path.relative_to(self.project_path)
                            location = str(rel_path)
                        except ValueError:
                            location = venv_path.name
                        
                        issues.append(Issue(
                            id=self._next_issue_id(),
                            severity=Severity.CRITICAL,
                            title=f"{location}/ inside project",
                            description=f"Virtual environment consuming {self._format_tokens(tokens)} tokens ({self._format_size(size)})",
                            path=venv_path,
                            tokens_impact=tokens,
                            fix_function="fix_venv_inside"
                        ))
        
        # Check for __pycache__
        pycache_dirs = list(self.project_path.rglob("__pycache__"))
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
        
        # Check for logs directory
        logs_path = self.project_path / "logs"
        if logs_path.exists() and logs_path.is_dir():
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
        
        # Check for .log files
        log_files = [f for f in self.project_path.rglob("*.log") if "venv" not in str(f)]
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
        
        # Check for node_modules
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
        large_files = []
        for ext in ["*.csv", "*.db", "*.sqlite", "*.sqlite3", "*.jsonl"]:
            for f in self.project_path.rglob(ext):
                if f.is_file() and f.stat().st_size > 1_000_000:  # > 1MB
                    large_files.append(f)
        
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
        
        # Check for external venv (must check this before other checks that use it)
        external_venv = self.venvs_dir / f"{self.project_name}-main"
        external_venv_exists = external_venv.exists()
        
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
        
        # Check for missing Cursor/VSCode settings
        vscode_settings = self.project_path / ".vscode" / "settings.json"
        if not vscode_settings.exists() and external_venv_exists:
            issues.append(Issue(
                id=self._next_issue_id(),
                severity=Severity.SUGGESTION,
                title="Missing Cursor/VSCode interpreter configuration",
                description="Cursor won't automatically use external venv",
                fix_function="fix_missing_vscode_settings"
            ))
        
        if not external_venv_exists and not issues:
            # No venv anywhere
            issues.append(Issue(
                id=self._next_issue_id(),
                severity=Severity.SUGGESTION,
                title="No virtual environment found",
                description=f"Expected at {external_venv}",
                fix_function="fix_create_venv"
            ))
        
        return DiagnosticReport(
            project_path=self.project_path,
            project_name=self.project_name,
            total_tokens=total_tokens,
            issues=issues,
            file_tokens=file_tokens_list,
            external_venv_exists=external_venv_exists,
            external_venv_path=external_venv if external_venv_exists else None
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
            # Show location being deleted
            try:
                rel_path = issue.path.relative_to(self.project_path)
                location = str(rel_path)
            except ValueError:
                location = issue.path.name
            
            shutil.rmtree(issue.path)
            print(COLORS.success(f"Deleted {location}/"))
            return True
        return False
    
    def fix_pycache(self, issue: Issue) -> bool:
        """Delete all __pycache__ directories."""
        count = 0
        for pycache in self.project_path.rglob("__pycache__"):
            shutil.rmtree(pycache)
            count += 1
        print(COLORS.success(f"Deleted {count} __pycache__ directories"))
        return True
    
    def fix_logs(self, issue: Issue) -> bool:
        """Archive logs to external location."""
        if issue.path and issue.path.exists():
            # Create artifacts directory
            logs_dest = self.artifacts_dir / "logs"
            logs_dest.mkdir(parents=True, exist_ok=True)
            
            # Move logs
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"logs_{timestamp}.tar.gz"
            
            with tarfile.open(logs_dest / archive_name, "w:gz") as tar:
                tar.add(issue.path, arcname="logs")
            
            shutil.rmtree(issue.path)
            issue.path.mkdir()  # Recreate empty logs dir
            (issue.path / ".gitkeep").touch()
            
            print(COLORS.success(f"Archived logs to {logs_dest / archive_name}"))
            return True
        return False
    
    def fix_log_files(self, issue: Issue) -> bool:
        """Delete scattered .log files."""
        count = 0
        for log_file in self.project_path.rglob("*.log"):
            if "venv" not in str(log_file):
                log_file.unlink()
                count += 1
        print(COLORS.success(f"Deleted {count} .log files"))
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
python -m pip install -U pip wheel

if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

echo "Done! Activate: source $VENV_DIR/bin/activate"
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

& "$VENV_DIR\\Scripts\\python.exe" -m pip install -U pip wheel

if (Test-Path .\\requirements.txt) {{
    & "$VENV_DIR\\Scripts\\pip.exe" install -r requirements.txt
}}

Write-Host "Done! Activate: $VENV_DIR\\Scripts\\Activate.ps1"
'''
        bootstrap_ps1.write_text(ps1_content, encoding="utf-8")
        
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
    
    def fix_missing_vscode_settings(self, issue: Issue) -> bool:
        """Create .vscode/settings.json with external venv path."""
        import json
        
        vscode_dir = self.project_path / ".vscode"
        vscode_dir.mkdir(exist_ok=True)
        
        settings_file = vscode_dir / "settings.json"
        
        # Determine venv path (relative to project)
        external_venv = self.venvs_dir / f"{self.project_name}-main"
        
        # Try to make path relative for portability
        try:
            rel_venv = external_venv.relative_to(self.project_path.parent)
            venv_path_str = f"../{rel_venv}"
        except ValueError:
            venv_path_str = str(external_venv)
        
        # Add appropriate Python executable path
        if os.name == "nt":  # Windows
            python_path = f"{venv_path_str}/Scripts/python.exe"
        else:  # Linux/Mac
            python_path = f"{venv_path_str}/bin/python"
        
        # Load existing settings or create new
        if settings_file.exists():
            try:
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
            except json.JSONDecodeError:
                settings = {}
        else:
            settings = {}
        
        # Update Python interpreter path
        settings["python.defaultInterpreterPath"] = python_path
        settings["python.terminal.activateEnvironment"] = True
        
        # Write settings
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
        
        print(COLORS.success(f"Created .vscode/settings.json with interpreter: {python_path}"))
        print(COLORS.info("   Cursor/VSCode will now use external venv automatically"))
        return True
    
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


def print_report(report: DiagnosticReport) -> None:
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
            
            # Add marker if movable
            marker = " 📦" if ft.is_movable else "   "
            line = f"{marker}{tokens_display} — {path_display}"[:65]
            print(f"║{line:<67}║")
        
        if len(high_token_files) > 20:
            remaining = len(high_token_files) - 20
            print(f"║  ... and {remaining} more files                                          ║")
    
    # Show movable files recommendations
    movable_files = [f for f in report.file_tokens if f.is_movable and f.tokens > 1000]
    if movable_files:
        print("╠══════════════════════════════════════════════════════════════════╣")
        print("║  📦 RECOMMENDED TO MOVE (can safely archive):                    ║")
        print("║                                                                  ║")
        
        total_movable_tokens = sum(f.tokens for f in movable_files)
        print(f"║  Potential savings: {total_movable_tokens/1000:.1f}K tokens                              ║")
        print("║                                                                  ║")
        
        for ft in movable_files[:10]:
            path_display = ft.relative_path
            if len(path_display) > 35:
                path_display = "..." + path_display[-32:]
            
            tokens_display = f"{ft.tokens/1000:.1f}K".rjust(6)
            reason = ft.move_reason[:18]
            line = f"  {tokens_display} — {path_display.ljust(36)} {reason}"[:65]
            print(f"║{line:<67}║")
        
        if len(movable_files) > 10:
            remaining = len(movable_files) - 10
            print(f"║  ... and {remaining} more movable files                                  ║")
        
        print("║                                                                  ║")
        print("║  💡 Tip: Move these to _AI_ARCHIVE/ to reduce AI context         ║")
    
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
    print_report(report)
    
    if report_only:
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
        
        # Re-diagnose
        after = doctor.diagnose()
        print_result(report, after, backup_path)
        
        # Update status
        update_status(project_path, skip_tests=True)
        print(COLORS.success("\nPROJECT_STATUS.md updated"))
        
        return True
    
    # Interactive mode
    while True:
        try:
            choice = input("\n> Enter choice: ").strip().upper()
        except (KeyboardInterrupt, EOFError):
            print("\n")
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
            
            # Re-diagnose
            after = doctor.diagnose()
            print_result(report, after, backup_path)
            
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

