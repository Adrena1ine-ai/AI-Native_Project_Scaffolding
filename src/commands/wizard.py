"""
🧙 Interactive Wizard v3.2 — Create & Optimize Projects
Implements SDD (Spec-Driven Development) and Doctor Mode
"""

from __future__ import annotations

import os
import re
import fnmatch
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

# Try to import rich for beautiful TUI
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from ..core.constants import COLORS, VERSION, TEMPLATES
from ..core.config import set_default_ide, get_default_ai_targets
from ..core.file_utils import create_file
from .create import create_project


# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════

WIZARD_TEMPLATES = [
    ("bot", "🤖 Telegram Bot", "aiogram 3.x, handlers, keyboards"),
    ("webapp", "🌐 Web App", "Telegram Mini App (HTML/JS/CSS)"),
    ("fastapi", "⚡ FastAPI", "REST API with SQLAlchemy"),
    ("parser", "🕷️ Parser", "Web scraper with aiohttp"),
    ("empty", "📦 Empty", "Minimal structure, no modules"),
]

RAW_EXCLUDE_DIRS = {".git", ".venv", "venv", "__pycache__"}

BINARY_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".so", ".dll", ".exe", ".bin",
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".zip", ".tar", ".gz", ".7z", ".rar", ".bz2",
    ".db", ".sqlite", ".sqlite3",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".mp3", ".mp4", ".wav", ".avi", ".mov",
}

# Strict cursorignore template for optimization
STRICT_CURSORIGNORE = '''# ═══════════════════════════════════════════════════════════════
# 🛑 CURSOR IGNORE — AI Toolkit Optimized
# Generated: {date}
# ═══════════════════════════════════════════════════════════════

# 1. VIRTUAL ENVIRONMENTS (Critical - saves ~500K tokens)
venv/**
.venv/**
env/**
**/site-packages/**

# 2. PYTHON RUNTIME
__pycache__/**
**/__pycache__/**
*.pyc
*.pyo
.pytest_cache/**
.mypy_cache/**
.ruff_cache/**

# 3. BUILD ARTIFACTS
dist/**
build/**
*.egg-info/**
*.whl
*.spec

# 4. SYSTEM / IDE
.git/**
.idea/**
.vscode/**
*.swp
*~
.DS_Store

# 5. DATA & LOGS
logs/**
*.log
data/**
*.csv
*.jsonl
*.sqlite
*.sqlite3
*.db

# 6. LOCK FILES
poetry.lock
Pipfile.lock
package-lock.json
yarn.lock

# 7. NODE MODULES
node_modules/**

# 8. SECRETS (Never index!)
.env
.env.*
!.env.example
*.pem
*.key

# ═══════════════════════════════════════════════════════════════
# ⚠️ DO NOT IGNORE: README.md, src/**, docs/**, config files
# ═══════════════════════════════════════════════════════════════
'''


# ═══════════════════════════════════════════════════════════════
# TOKEN UTILITIES (from benchmark.py)
# ═══════════════════════════════════════════════════════════════

@dataclass
class ScanResult:
    """Result of a directory scan"""
    file_count: int
    total_chars: int
    total_tokens: int
    
    @property
    def formatted_tokens(self) -> str:
        if self.total_tokens >= 1_000_000:
            return f"{self.total_tokens / 1_000_000:.1f}M"
        elif self.total_tokens >= 1_000:
            return f"{self.total_tokens / 1_000:.1f}K"
        return str(self.total_tokens)


def parse_ignore_patterns(path: Path) -> list[str]:
    """Parse .cursorignore patterns"""
    ignore_file = path / ".cursorignore"
    patterns = []
    
    if not ignore_file.exists():
        return patterns
    
    try:
        content = ignore_file.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("!"):
                continue
            patterns.append(line)
    except Exception:
        pass
    
    return patterns


def should_ignore(path: Path, root: Path, patterns: list[str]) -> bool:
    """Check if path should be ignored"""
    if not patterns:
        return False
    
    try:
        rel_path = path.relative_to(root)
    except ValueError:
        return False
    
    rel_str = str(rel_path)
    name = path.name
    
    for pattern in patterns:
        if pattern.endswith("/"):
            dir_pattern = pattern.rstrip("/")
            if fnmatch.fnmatch(name, dir_pattern):
                return True
            if rel_str.startswith(dir_pattern + "/") or rel_str == dir_pattern:
                return True
        
        if pattern.startswith("**/"):
            sub_pattern = pattern[3:]
            if fnmatch.fnmatch(name, sub_pattern):
                return True
            for part in rel_path.parts:
                if fnmatch.fnmatch(part, sub_pattern):
                    return True
        
        if fnmatch.fnmatch(name, pattern):
            return True
        if fnmatch.fnmatch(rel_str, pattern):
            return True
        
        if "*" not in pattern and "/" not in pattern:
            if pattern in rel_path.parts:
                return True
    
    return False


def scan_directory(root: Path, ignore_patterns: list[str] | None = None) -> ScanResult:
    """Scan directory and count files/tokens"""
    file_count = 0
    total_chars = 0
    
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        
        # Filter directories
        dirnames[:] = [
            d for d in dirnames 
            if d not in RAW_EXCLUDE_DIRS
            and not (ignore_patterns and should_ignore(current / d, root, ignore_patterns))
        ]
        
        for filename in filenames:
            file_path = current / filename
            
            if ignore_patterns and should_ignore(file_path, root, ignore_patterns):
                continue
            
            ext = file_path.suffix.lower()
            if ext in BINARY_EXTENSIONS:
                continue
            
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                file_count += 1
                total_chars += len(content)
            except (PermissionError, OSError):
                continue
    
    return ScanResult(
        file_count=file_count,
        total_chars=total_chars,
        total_tokens=total_chars // 4
    )


# ═══════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════

def validate_project_name(name: str) -> tuple[bool, str]:
    """Validate project name"""
    if not name:
        return False, "Name cannot be empty"
    if " " in name:
        return False, "Name cannot contain spaces"
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', name):
        return False, "Name must start with letter, contain only letters/numbers/_/-"
    if len(name) > 50:
        return False, "Name too long (max 50 chars)"
    return True, ""


# ═══════════════════════════════════════════════════════════════
# SPEC.MD GENERATION (SDD)
# ═══════════════════════════════════════════════════════════════

def generate_spec_md(
    project_dir: Path,
    name: str,
    template: str,
    description: str
) -> None:
    """Generate spec.md for Spec-Driven Development"""
    
    template_info = dict(WIZARD_TEMPLATES).get(template, ("", "Unknown"))
    if isinstance(template_info, tuple):
        stack_info = template_info[1] if len(template_info) > 1 else ""
    else:
        stack_info = template_info
    
    content = f'''# 📋 Project Specification — {name}

> Generated by AI Toolkit v{VERSION} on {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 🎯 Goal

{description if description else "TODO: Describe the main purpose of this project."}

---

## 🛠️ Tech Stack

- **Template:** {template}
- **Stack:** {stack_info}
- **Python:** 3.10+
- **Package Manager:** pip + requirements.txt

---

## 📁 Structure

```
{name}/
├── _AI_INCLUDE/      # AI context files
├── scripts/          # Bootstrap & utilities
├── {template}/       # Main module
├── config.py         # Configuration
├── requirements.txt  # Dependencies
└── spec.md           # This file
```

---

## 🤖 AI Context Priming

When working on this project, the AI should:

1. **Read first:** `_AI_INCLUDE/PROJECT_CONVENTIONS.md`
2. **Understand:** This is a {template} project focused on {description[:100] if description else "TODO"}
3. **Remember:** venv is stored OUTSIDE the project in `../_venvs/{name}-venv/`
4. **Follow:** Python best practices, type hints, docstrings

---

## 📝 TODO

- [ ] Configure `.env` with required secrets
- [ ] Review generated code structure
- [ ] Implement core functionality
- [ ] Add tests
- [ ] Update this spec with specific requirements

---

*This file serves as the "north star" for AI assistants working on this project.*
'''
    
    create_file(project_dir / "spec.md", content, quiet=True)


# ═══════════════════════════════════════════════════════════════
# OPTIMIZATION LOG GENERATION
# ═══════════════════════════════════════════════════════════════

def generate_optimization_log(
    project_dir: Path,
    before: ScanResult,
    after: ScanResult,
    changes: list[str]
) -> None:
    """Generate OPTIMIZATION_LOG.md summarizing changes"""
    
    tokens_saved = before.total_tokens - after.total_tokens
    pct_saved = (tokens_saved / before.total_tokens * 100) if before.total_tokens > 0 else 0
    
    content = f'''# 🏥 Optimization Log

> Generated by AI Toolkit v{VERSION} on {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 📊 Results

| Metric | Before | After | Saved |
|--------|--------|-------|-------|
| Files | {before.file_count} | {after.file_count} | -{before.file_count - after.file_count} |
| Tokens | {before.formatted_tokens} | {after.formatted_tokens} | -{tokens_saved // 1000}K ({pct_saved:.1f}%) |

---

## 🔧 Changes Applied

'''
    
    for change in changes:
        content += f"- {change}\n"
    
    content += f'''
---

## 🤖 For AI Assistants

This project has been optimized for AI context. Key points:

1. **Token budget reduced by {pct_saved:.1f}%**
2. **Hidden from context:** venv, __pycache__, logs, data files
3. **Visible to AI:** src/, docs/, config files, README.md
4. **Rules location:** `.cursor/rules/` or `.cursorrules`

When working on this project, respect the `.cursorignore` patterns.

---

*Optimization performed by AI Toolkit Doctor Mode.*
'''
    
    create_file(project_dir / "OPTIMIZATION_LOG.md", content, quiet=True)


# ═══════════════════════════════════════════════════════════════
# FLOW A: CREATE NEW PROJECT (Rich)
# ═══════════════════════════════════════════════════════════════

def flow_create_rich(console: Console) -> bool:
    """Create new project flow with rich UI"""
    
    console.print(Panel(
        "[bold cyan]🐣 Create New Project[/bold cyan]\n"
        "[dim]Start fresh with an AI-optimized structure[/dim]",
        border_style="cyan"
    ))
    console.print()
    
    # Step 1: Project Name
    console.print("[bold]📝 Step 1/4: Project Name[/bold]")
    while True:
        name = Prompt.ask("  [cyan]Name[/cyan]", default="my_bot")
        is_valid, error = validate_project_name(name)
        if is_valid:
            console.print(f"  [green]✓[/green] {name}\n")
            break
        console.print(f"  [red]✗ {error}[/red]")
    
    # Step 2: Template
    console.print("[bold]📦 Step 2/4: Template[/bold]")
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    table.add_column("", width=3)
    table.add_column("", width=18)
    table.add_column("", style="dim")
    for i, (_, icon_name, desc) in enumerate(WIZARD_TEMPLATES, 1):
        table.add_row(f"[cyan]{i}[/cyan]", icon_name, desc)
    console.print(table)
    
    choice = Prompt.ask("  [cyan]Choice[/cyan]", choices=["1","2","3","4","5"], default="1")
    template_key, template_name, _ = WIZARD_TEMPLATES[int(choice) - 1]
    console.print(f"  [green]✓[/green] {template_name}\n")
    
    # Step 3: Description (SDD)
    console.print("[bold]📋 Step 3/4: Project Description (for AI)[/bold]")
    console.print("  [dim]Briefly describe the goal and stack. This helps AI understand context.[/dim]")
    description = Prompt.ask("  [cyan]Description[/cyan]", default="")
    if description:
        console.print(f"  [green]✓[/green] Saved\n")
    else:
        console.print(f"  [yellow]○[/yellow] Skipped\n")
    
    # Step 4: Options
    console.print("[bold]⚙️ Step 4/4: Options[/bold]")
    include_git = Confirm.ask("  [cyan]Git?[/cyan]", default=True)
    include_docker = Confirm.ask("  [cyan]Docker?[/cyan]", default=True)
    include_ci = Confirm.ask("  [cyan]CI/CD?[/cyan]", default=True)
    console.print()
    
    # Summary
    summary = Table(box=box.ROUNDED, show_header=False, border_style="green")
    summary.add_column("", style="cyan")
    summary.add_column("", style="bold")
    summary.add_row("📁 Project", name)
    summary.add_row("📦 Template", template_name)
    summary.add_row("📂 Location", str(Path.cwd() / name))
    summary.add_row("📋 Description", description[:40] + "..." if len(description) > 40 else (description or "-"))
    summary.add_row("🔗 Git/Docker/CI", f"{'✓' if include_git else '✗'} / {'✓' if include_docker else '✗'} / {'✓' if include_ci else '✗'}")
    
    console.print(Panel(summary, title="[bold]Summary[/bold]", border_style="green"))
    console.print()
    
    if not Confirm.ask("  [bold]Create project?[/bold]", default=True):
        console.print("  [yellow]Cancelled.[/yellow]\n")
        return False
    
    console.print()
    
    # Create project
    set_default_ide("all", ["cursor", "copilot", "claude", "windsurf"])
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        progress.add_task("Creating project...", total=None)
        
        success = create_project(
            name=name,
            path=Path.cwd(),
            template=template_key if template_key != "empty" else "bot",
            ai_targets=get_default_ai_targets(),
            include_docker=include_docker,
            include_ci=include_ci,
            include_git=include_git,
        )
        
        if success and description:
            generate_spec_md(Path.cwd() / name, name, template_key, description)
    
    if success:
        console.print(Panel(
            f"[bold green]🎉 Project created![/bold green]\n\n"
            f"[dim]Next steps:[/dim]\n"
            f"  [cyan]cd {name}[/cyan]\n"
            f"  [cyan]./scripts/bootstrap.sh[/cyan]\n"
            f"  [cyan]source ../_venvs/{name}-venv/bin/activate[/cyan]",
            border_style="green"
        ))
    
    return success


# ═══════════════════════════════════════════════════════════════
# FLOW B: OPTIMIZE EXISTING PROJECT (Rich)
# ═══════════════════════════════════════════════════════════════

def flow_optimize_rich(console: Console) -> bool:
    """Optimize existing project flow with rich UI"""
    
    console.print(Panel(
        "[bold magenta]🚑 Optimize Existing Project[/bold magenta]\n"
        "[dim]Add AI-friendly rules and reduce token usage[/dim]",
        border_style="magenta"
    ))
    console.print()
    
    # Step 1: Project Path
    console.print("[bold]📂 Step 1/2: Project Path[/bold]")
    path_str = Prompt.ask("  [cyan]Path[/cyan]", default=".")
    project_path = Path(path_str).resolve()
    
    if not project_path.exists():
        console.print(f"  [red]✗ Path does not exist[/red]\n")
        return False
    
    if not project_path.is_dir():
        console.print(f"  [red]✗ Not a directory[/red]\n")
        return False
    
    console.print(f"  [green]✓[/green] {project_path}\n")
    
    # Step 2: Analysis
    console.print("[bold]🔍 Step 2/2: Analyzing...[/bold]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("Scanning files...", total=None)
        before = scan_directory(project_path)
        progress.update(task, description="Analysis complete")
    
    console.print(f"  📁 Files: [bold]{before.file_count}[/bold]")
    console.print(f"  🎯 Tokens: [bold]{before.formatted_tokens}[/bold]")
    console.print()
    
    # Show what will be done
    changes_preview = []
    
    cursorignore_exists = (project_path / ".cursorignore").exists()
    if cursorignore_exists:
        changes_preview.append("📝 Update .cursorignore with strict rules")
    else:
        changes_preview.append("📝 Create .cursorignore (strict template)")
    
    cursor_rules_dir = project_path / ".cursor" / "rules"
    if not cursor_rules_dir.exists():
        changes_preview.append("📁 Create .cursor/rules/ structure")
    
    changes_preview.append("📊 Generate OPTIMIZATION_LOG.md")
    
    console.print("[bold]📋 Planned Changes:[/bold]")
    for change in changes_preview:
        console.print(f"  • {change}")
    console.print()
    
    if not Confirm.ask("  [bold]Apply optimization?[/bold]", default=True):
        console.print("  [yellow]Cancelled.[/yellow]\n")
        return False
    
    console.print()
    
    # Apply changes
    changes_made = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("Applying...", total=None)
        
        # 1. Create/update .cursorignore
        progress.update(task, description="Creating .cursorignore...")
        cursorignore_content = STRICT_CURSORIGNORE.format(
            date=datetime.now().strftime("%Y-%m-%d")
        )
        create_file(project_path / ".cursorignore", cursorignore_content, quiet=True)
        changes_made.append("Created/updated .cursorignore with strict rules")
        
        # 2. Create .cursor/rules/ structure
        progress.update(task, description="Creating rules structure...")
        cursor_rules_dir.mkdir(parents=True, exist_ok=True)
        
        # project.md
        project_name = project_path.name
        project_md = f'''# 📋 Project Context — {project_name}

## Overview

This project has been optimized by AI Toolkit for efficient AI assistance.

## Key Files

| Purpose | Location |
|---------|----------|
| Source code | `src/` or root `.py` files |
| Configuration | `config.py`, `.env` |
| Documentation | `README.md`, `docs/` |
| AI Rules | `.cursorrules`, `.cursor/rules/` |

## Conventions

- Python 3.10+ with type hints
- English only (no Russian text)
- PEP 8 formatting
- Docstrings for public functions
'''
        create_file(cursor_rules_dir / "project.md", project_md, quiet=True)
        changes_made.append("Created .cursor/rules/project.md")
        
        # style.md
        style_md = '''# 🎨 Code Style Guide

## Python

- Use type hints for all functions
- Write docstrings (Google style)
- Max line length: 100 characters
- Use `pathlib.Path` for file operations

## Naming

- `snake_case` for functions/variables
- `PascalCase` for classes
- `UPPER_CASE` for constants

## Imports

```python
# Standard library
from pathlib import Path

# Third-party
import requests

# Local
from .module import function
```
'''
        create_file(cursor_rules_dir / "style.md", style_md, quiet=True)
        changes_made.append("Created .cursor/rules/style.md")
        
        # 3. Rescan with new ignore rules
        progress.update(task, description="Measuring improvement...")
        new_patterns = parse_ignore_patterns(project_path)
        after = scan_directory(project_path, new_patterns)
        
        # 4. Generate optimization log
        progress.update(task, description="Generating report...")
        generate_optimization_log(project_path, before, after, changes_made)
        changes_made.append("Generated OPTIMIZATION_LOG.md")
    
    # Results
    tokens_saved = before.total_tokens - after.total_tokens
    pct_saved = (tokens_saved / before.total_tokens * 100) if before.total_tokens > 0 else 0
    
    result_table = Table(box=box.ROUNDED, show_header=True, border_style="green")
    result_table.add_column("Metric", style="cyan")
    result_table.add_column("Before", justify="right", style="red")
    result_table.add_column("After", justify="right", style="green")
    result_table.add_column("Saved", justify="right", style="yellow")
    
    result_table.add_row(
        "📁 Files",
        str(before.file_count),
        str(after.file_count),
        f"-{before.file_count - after.file_count}"
    )
    result_table.add_row(
        "🎯 Tokens",
        before.formatted_tokens,
        after.formatted_tokens,
        f"-{tokens_saved // 1000}K ({pct_saved:.1f}%)"
    )
    
    console.print(Panel(
        result_table,
        title="[bold green]✅ Optimization Complete[/bold green]",
        border_style="green"
    ))
    console.print()
    
    console.print(f"  📄 See [cyan]OPTIMIZATION_LOG.md[/cyan] for details\n")
    
    return True


# ═══════════════════════════════════════════════════════════════
# MAIN WIZARD ENTRY POINT
# ═══════════════════════════════════════════════════════════════

def run_wizard_rich() -> bool:
    """Run wizard with rich UI"""
    console = Console()
    
    # Header
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]🧙 AI Toolkit Wizard v{VERSION}[/bold cyan]\n"
        "[dim]Create & Optimize AI-friendly projects[/dim]",
        border_style="cyan",
        box=box.DOUBLE
    ))
    console.print()
    
    # Entry point: What would you like to do?
    console.print("[bold]What would you like to do?[/bold]\n")
    console.print("  [cyan]1.[/cyan] 🐣 [bold]Create New Project[/bold] — Start fresh")
    console.print("  [cyan]2.[/cyan] 🚑 [bold]Optimize Existing Project[/bold] — Doctor mode")
    console.print()
    
    choice = Prompt.ask("  [cyan]Choice[/cyan]", choices=["1", "2"], default="1")
    console.print()
    
    if choice == "1":
        return flow_create_rich(console)
    else:
        return flow_optimize_rich(console)


def run_wizard_plain() -> bool:
    """Run wizard with plain text (fallback)"""
    print(f"""
{COLORS.colorize('═' * 50, COLORS.CYAN)}
{COLORS.colorize(f'🧙 AI Toolkit Wizard v{VERSION}', COLORS.CYAN)}
{COLORS.colorize('═' * 50, COLORS.CYAN)}
""")
    
    print("What would you like to do?\n")
    print(f"  {COLORS.colorize('1.', COLORS.CYAN)} 🐣 Create New Project")
    print(f"  {COLORS.colorize('2.', COLORS.CYAN)} 🚑 Optimize Existing Project")
    print()
    
    choice = input("  Choice [1]: ").strip() or "1"
    print()
    
    if choice == "1":
        return flow_create_plain()
    elif choice == "2":
        return flow_optimize_plain()
    else:
        print(f"  {COLORS.error('Invalid choice')}")
        return False


def flow_create_plain() -> bool:
    """Create flow with plain text"""
    print(f"{COLORS.colorize('🐣 Create New Project', COLORS.CYAN)}\n")
    
    # Name
    while True:
        name = input("  Project name [my_bot]: ").strip() or "my_bot"
        is_valid, error = validate_project_name(name)
        if is_valid:
            print(f"  {COLORS.success(f'✓ {name}')}\n")
            break
        print(f"  {COLORS.error(f'✗ {error}')}")
    
    # Template
    print("  Template:")
    for i, (_, icon_name, desc) in enumerate(WIZARD_TEMPLATES, 1):
        print(f"    {i}. {icon_name} — {desc}")
    choice = input("  Choice [1]: ").strip() or "1"
    try:
        template_key, template_name, _ = WIZARD_TEMPLATES[int(choice) - 1]
    except (ValueError, IndexError):
        template_key, template_name, _ = WIZARD_TEMPLATES[0]
    print(f"  {COLORS.success(f'✓ {template_name}')}\n")
    
    # Description
    description = input("  Description (for AI): ").strip()
    print()
    
    # Options
    include_git = input("  Git? (Y/n): ").strip().lower() != 'n'
    include_docker = input("  Docker? (Y/n): ").strip().lower() != 'n'
    include_ci = input("  CI/CD? (Y/n): ").strip().lower() != 'n'
    print()
    
    # Confirm
    if input("  Create? (Y/n): ").strip().lower() == 'n':
        print(f"  {COLORS.warning('Cancelled.')}\n")
        return False
    
    print()
    
    # Create
    set_default_ide("all", ["cursor", "copilot", "claude", "windsurf"])
    success = create_project(
        name=name,
        path=Path.cwd(),
        template=template_key if template_key != "empty" else "bot",
        ai_targets=get_default_ai_targets(),
        include_docker=include_docker,
        include_ci=include_ci,
        include_git=include_git,
    )
    
    if success and description:
        generate_spec_md(Path.cwd() / name, name, template_key, description)
    
    return success


def flow_optimize_plain() -> bool:
    """Optimize flow with plain text"""
    print(f"{COLORS.colorize('🚑 Optimize Existing Project', COLORS.MAGENTA)}\n")
    
    path_str = input("  Project path [.]: ").strip() or "."
    project_path = Path(path_str).resolve()
    
    if not project_path.exists() or not project_path.is_dir():
        print(f"  {COLORS.error('Invalid path')}\n")
        return False
    
    print(f"  {COLORS.success(f'✓ {project_path}')}\n")
    
    # Scan
    print("  Analyzing...")
    before = scan_directory(project_path)
    print(f"  📁 Files: {before.file_count}")
    print(f"  🎯 Tokens: {before.formatted_tokens}\n")
    
    if input("  Apply optimization? (Y/n): ").strip().lower() == 'n':
        print(f"  {COLORS.warning('Cancelled.')}\n")
        return False
    
    print()
    changes_made = []
    
    # Apply
    cursorignore_content = STRICT_CURSORIGNORE.format(
        date=datetime.now().strftime("%Y-%m-%d")
    )
    create_file(project_path / ".cursorignore", cursorignore_content, quiet=True)
    changes_made.append("Created .cursorignore")
    
    cursor_rules_dir = project_path / ".cursor" / "rules"
    cursor_rules_dir.mkdir(parents=True, exist_ok=True)
    create_file(cursor_rules_dir / "project.md", f"# {project_path.name}\n\nOptimized by AI Toolkit.", quiet=True)
    changes_made.append("Created .cursor/rules/")
    
    new_patterns = parse_ignore_patterns(project_path)
    after = scan_directory(project_path, new_patterns)
    
    generate_optimization_log(project_path, before, after, changes_made)
    
    tokens_saved = before.total_tokens - after.total_tokens
    pct_saved = (tokens_saved / before.total_tokens * 100) if before.total_tokens > 0 else 0
    
    print(f"{COLORS.colorize('✅ Optimization Complete', COLORS.GREEN)}")
    print(f"  Before: {before.formatted_tokens} → After: {after.formatted_tokens}")
    print(f"  Saved: {tokens_saved // 1000}K tokens ({pct_saved:.1f}%)\n")
    
    return True


def run_wizard() -> bool:
    """Run the interactive wizard"""
    if HAS_RICH:
        return run_wizard_rich()
    else:
        return run_wizard_plain()


def cmd_wizard() -> None:
    """Interactive wizard command wrapper"""
    run_wizard()
