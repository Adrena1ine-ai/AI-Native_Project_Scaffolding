#!/usr/bin/env python3
"""
🔬 Token Benchmark — Compare Raw vs Optimized Project Scans

This script demonstrates the token savings achieved by using .cursorignore
to optimize what the AI sees in your project.

Usage:
    python benchmark.py [path]
    python benchmark.py              # Scan current directory
    python benchmark.py ./my_project # Scan specific project
"""

from __future__ import annotations

import os
import sys
import fnmatch
from pathlib import Path
from dataclasses import dataclass

# Try to import rich for pretty output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None


# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# Baseline directories to always exclude (even in raw mode)
RAW_EXCLUDE_DIRS = {".git", ".venv", "venv", "__pycache__"}

# Cost per 1M input tokens (GPT-4 baseline)
COST_PER_MILLION_TOKENS = 15.0

# Binary/non-text extensions to skip
BINARY_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".so", ".dll", ".exe", ".bin",
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".zip", ".tar", ".gz", ".7z", ".rar", ".bz2",
    ".db", ".sqlite", ".sqlite3",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".mp3", ".mp4", ".wav", ".avi", ".mov",
}


@dataclass
class ScanResult:
    """Result of a directory scan"""
    file_count: int
    total_chars: int
    total_tokens: int
    files_by_ext: dict[str, int]
    
    @property
    def estimated_cost(self) -> float:
        """Estimated cost in USD"""
        return (self.total_tokens / 1_000_000) * COST_PER_MILLION_TOKENS


def estimate_tokens(char_count: int) -> int:
    """Approximate token count (1 token ≈ 4 characters)"""
    return char_count // 4


def parse_cursorignore(path: Path) -> list[str]:
    """
    Parse .cursorignore file and return list of patterns
    
    Args:
        path: Path to project root
        
    Returns:
        List of ignore patterns
    """
    ignore_file = path / ".cursorignore"
    patterns = []
    
    if not ignore_file.exists():
        return patterns
    
    try:
        content = ignore_file.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            # Skip negation patterns (not supported in simple fnmatch)
            if line.startswith("!"):
                continue
            patterns.append(line)
    except Exception:
        pass
    
    return patterns


def should_ignore(path: Path, root: Path, patterns: list[str]) -> bool:
    """
    Check if a path should be ignored based on patterns
    
    Args:
        path: File or directory path
        root: Project root path
        patterns: List of ignore patterns
        
    Returns:
        True if path should be ignored
    """
    if not patterns:
        return False
    
    # Get relative path from root
    try:
        rel_path = path.relative_to(root)
    except ValueError:
        return False
    
    rel_str = str(rel_path)
    name = path.name
    
    for pattern in patterns:
        # Handle directory patterns (ending with /)
        if pattern.endswith("/"):
            dir_pattern = pattern.rstrip("/")
            # Check if any part of the path matches
            if fnmatch.fnmatch(name, dir_pattern):
                return True
            if fnmatch.fnmatch(rel_str, f"*/{dir_pattern}/*"):
                return True
            if fnmatch.fnmatch(rel_str, f"{dir_pattern}/*"):
                return True
            if rel_str.startswith(dir_pattern + "/") or rel_str == dir_pattern:
                return True
        
        # Handle ** patterns (recursive)
        if pattern.startswith("**/"):
            sub_pattern = pattern[3:]
            if fnmatch.fnmatch(name, sub_pattern):
                return True
            if fnmatch.fnmatch(rel_str, sub_pattern):
                return True
            # Check each path component
            for part in rel_path.parts:
                if fnmatch.fnmatch(part, sub_pattern):
                    return True
        
        # Direct pattern match
        if fnmatch.fnmatch(name, pattern):
            return True
        if fnmatch.fnmatch(rel_str, pattern):
            return True
        
        # Check if pattern matches any directory in path
        if "*" not in pattern and "/" not in pattern:
            if pattern in rel_path.parts:
                return True
    
    return False


def scan_directory(
    root: Path,
    exclude_dirs: set[str],
    ignore_patterns: list[str] | None = None
) -> ScanResult:
    """
    Scan directory and count files/tokens
    
    Args:
        root: Directory to scan
        exclude_dirs: Set of directory names to always exclude
        ignore_patterns: Optional list of .cursorignore patterns
        
    Returns:
        ScanResult with counts
    """
    file_count = 0
    total_chars = 0
    files_by_ext: dict[str, int] = {}
    
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        
        # Filter out excluded directories (in-place)
        dirnames[:] = [
            d for d in dirnames 
            if d not in exclude_dirs
            and not (ignore_patterns and should_ignore(current / d, root, ignore_patterns))
        ]
        
        for filename in filenames:
            file_path = current / filename
            
            # Skip if ignored by patterns
            if ignore_patterns and should_ignore(file_path, root, ignore_patterns):
                continue
            
            # Skip binary files
            ext = file_path.suffix.lower()
            if ext in BINARY_EXTENSIONS:
                continue
            
            # Try to read file
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                char_count = len(content)
                
                file_count += 1
                total_chars += char_count
                
                # Track by extension
                ext_key = ext if ext else "(no ext)"
                files_by_ext[ext_key] = files_by_ext.get(ext_key, 0) + 1
                
            except (PermissionError, OSError, UnicodeDecodeError):
                continue
    
    return ScanResult(
        file_count=file_count,
        total_chars=total_chars,
        total_tokens=estimate_tokens(total_chars),
        files_by_ext=files_by_ext
    )


def format_number(n: int) -> str:
    """Format number with thousand separators"""
    return f"{n:,}"


def format_tokens(tokens: int) -> str:
    """Format token count with K/M suffix"""
    if tokens >= 1_000_000:
        return f"{tokens / 1_000_000:.1f}M"
    elif tokens >= 1_000:
        return f"{tokens / 1_000:.1f}K"
    return str(tokens)


def print_results_rich(
    raw: ScanResult,
    optimized: ScanResult,
    has_cursorignore: bool,
    project_path: Path
) -> None:
    """Print results using rich library"""
    
    # Calculate savings
    files_saved = raw.file_count - optimized.file_count
    tokens_saved = raw.total_tokens - optimized.total_tokens
    pct_saved = (tokens_saved / raw.total_tokens * 100) if raw.total_tokens > 0 else 0
    cost_saved = raw.estimated_cost - optimized.estimated_cost
    
    # Header
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]🔬 Token Benchmark[/bold cyan]\n"
        f"[dim]Project: {project_path}[/dim]",
        border_style="cyan"
    ))
    console.print()
    
    # Comparison table
    table = Table(
        title="📊 Comparison: Raw vs Optimized",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("Metric", style="cyan", width=25)
    table.add_column("Mode A (Raw)", justify="right", style="red")
    table.add_column("Mode B (Optimized)", justify="right", style="green")
    table.add_column("Savings", justify="right", style="yellow")
    
    table.add_row(
        "📁 Files",
        format_number(raw.file_count),
        format_number(optimized.file_count),
        f"-{format_number(files_saved)}"
    )
    
    table.add_row(
        "📝 Characters",
        format_number(raw.total_chars),
        format_number(optimized.total_chars),
        f"-{format_number(raw.total_chars - optimized.total_chars)}"
    )
    
    table.add_row(
        "🎯 Tokens (est.)",
        format_tokens(raw.total_tokens),
        format_tokens(optimized.total_tokens),
        f"-{format_tokens(tokens_saved)} ({pct_saved:.1f}%)"
    )
    
    table.add_row(
        "💰 Cost (GPT-4 input)",
        f"${raw.estimated_cost:.4f}",
        f"${optimized.estimated_cost:.4f}",
        f"-${cost_saved:.4f}"
    )
    
    console.print(table)
    console.print()
    
    # Status
    if not has_cursorignore:
        console.print(
            "[yellow]⚠️  No .cursorignore found![/yellow] "
            "Mode A = Mode B (no optimization)\n"
            "[dim]Run [cyan]ai-toolkit[/cyan] to create optimized project structure.[/dim]"
        )
    elif pct_saved > 0:
        console.print(
            f"[green]✅ Optimization active![/green] "
            f"Saving [bold]{pct_saved:.1f}%[/bold] of tokens "
            f"([bold]{format_tokens(tokens_saved)}[/bold] tokens per full context load)"
        )
    else:
        console.print(
            "[cyan]ℹ️  No significant savings[/cyan] — "
            "project is already minimal or .cursorignore needs tuning."
        )
    
    console.print()
    
    # Top extensions
    if optimized.files_by_ext:
        ext_table = Table(
            title="📦 File Types (Optimized View)",
            box=box.SIMPLE,
            show_header=True
        )
        ext_table.add_column("Extension", style="cyan")
        ext_table.add_column("Count", justify="right")
        
        sorted_ext = sorted(
            optimized.files_by_ext.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        for ext, count in sorted_ext:
            ext_table.add_row(ext, str(count))
        
        console.print(ext_table)
        console.print()


def print_results_plain(
    raw: ScanResult,
    optimized: ScanResult,
    has_cursorignore: bool,
    project_path: Path
) -> None:
    """Print results using plain text"""
    
    # Calculate savings
    files_saved = raw.file_count - optimized.file_count
    tokens_saved = raw.total_tokens - optimized.total_tokens
    pct_saved = (tokens_saved / raw.total_tokens * 100) if raw.total_tokens > 0 else 0
    cost_saved = raw.estimated_cost - optimized.estimated_cost
    
    print()
    print("=" * 60)
    print("🔬 TOKEN BENCHMARK")
    print(f"   Project: {project_path}")
    print("=" * 60)
    print()
    
    # Table header
    print("📊 Comparison: Raw vs Optimized")
    print("-" * 60)
    print(f"{'Metric':<25} {'Raw':>12} {'Optimized':>12} {'Savings':>12}")
    print("-" * 60)
    
    print(f"{'📁 Files':<25} {raw.file_count:>12,} {optimized.file_count:>12,} {-files_saved:>+12,}")
    print(f"{'📝 Characters':<25} {raw.total_chars:>12,} {optimized.total_chars:>12,} {-(raw.total_chars - optimized.total_chars):>+12,}")
    print(f"{'🎯 Tokens (est.)':<25} {format_tokens(raw.total_tokens):>12} {format_tokens(optimized.total_tokens):>12} {'-' + format_tokens(tokens_saved) + f' ({pct_saved:.1f}%)':>12}")
    print(f"{'💰 Cost (GPT-4)':<25} {'$' + f'{raw.estimated_cost:.4f}':>11} {'$' + f'{optimized.estimated_cost:.4f}':>11} {'-$' + f'{cost_saved:.4f}':>11}")
    
    print("-" * 60)
    print()
    
    # Status
    if not has_cursorignore:
        print("⚠️  No .cursorignore found! Mode A = Mode B (no optimization)")
        print("   Run 'ai-toolkit' to create optimized project structure.")
    elif pct_saved > 0:
        print(f"✅ Optimization active! Saving {pct_saved:.1f}% of tokens")
        print(f"   ({format_tokens(tokens_saved)} tokens per full context load)")
    else:
        print("ℹ️  No significant savings — project is already minimal")
    
    print()


def run_benchmark(project_path: Path | None = None) -> int:
    """
    Run the benchmark
    
    Args:
        project_path: Path to project (defaults to current directory)
        
    Returns:
        Exit code (0 = success)
    """
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path).resolve()
    
    if not project_path.exists():
        print(f"❌ Path does not exist: {project_path}")
        return 1
    
    if not project_path.is_dir():
        print(f"❌ Path is not a directory: {project_path}")
        return 1
    
    # Check for .cursorignore
    has_cursorignore = (project_path / ".cursorignore").exists()
    ignore_patterns = parse_cursorignore(project_path) if has_cursorignore else []
    
    # Mode A: Raw scan (minimal exclusions)
    raw_result = scan_directory(
        root=project_path,
        exclude_dirs=RAW_EXCLUDE_DIRS,
        ignore_patterns=None
    )
    
    # Mode B: Optimized scan (respects .cursorignore)
    if has_cursorignore and ignore_patterns:
        optimized_result = scan_directory(
            root=project_path,
            exclude_dirs=RAW_EXCLUDE_DIRS,
            ignore_patterns=ignore_patterns
        )
    else:
        # No cursorignore = same as raw
        optimized_result = raw_result
    
    # Print results
    if HAS_RICH:
        print_results_rich(raw_result, optimized_result, has_cursorignore, project_path)
    else:
        print_results_plain(raw_result, optimized_result, has_cursorignore, project_path)
    
    return 0


def main() -> int:
    """Main entry point"""
    # Parse command line args
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h", "--help"):
            print(__doc__)
            return 0
        project_path = Path(sys.argv[1])
    else:
        project_path = None
    
    return run_benchmark(project_path)


if __name__ == "__main__":
    sys.exit(main())

