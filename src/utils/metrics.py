"""
📊 Metrics — Project scanning and token estimation
"""

from __future__ import annotations

import os
import fnmatch
from pathlib import Path
from dataclasses import dataclass


# Directories to always exclude from scanning
EXCLUDE_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", "_AI_ARCHIVE"}

# Binary extensions to skip
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
    """Result of a project scan"""
    files_count: int
    char_count: int
    token_est: int
    
    @property
    def formatted_tokens(self) -> str:
        """Format token count with K/M suffix"""
        if self.token_est >= 1_000_000:
            return f"{self.token_est / 1_000_000:.1f}M"
        elif self.token_est >= 1_000:
            return f"{self.token_est / 1_000:.1f}K"
        return str(self.token_est)
    
    @property
    def formatted_size(self) -> str:
        """Format character count as size"""
        if self.char_count >= 1_000_000:
            return f"{self.char_count / 1_000_000:.1f}MB"
        elif self.char_count >= 1_000:
            return f"{self.char_count / 1_000:.1f}KB"
        return f"{self.char_count}B"


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
            if not line or line.startswith("#") or line.startswith("!"):
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
            if fnmatch.fnmatch(name, dir_pattern):
                return True
            if rel_str.startswith(dir_pattern + "/") or rel_str == dir_pattern:
                return True
        
        # Handle ** patterns (recursive)
        if pattern.startswith("**/"):
            sub_pattern = pattern[3:]
            if fnmatch.fnmatch(name, sub_pattern):
                return True
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


def scan_project(path: Path) -> ScanResult:
    """
    Scan project and return metrics
    
    Args:
        path: Path to project root
        
    Returns:
        ScanResult with files_count, char_count, token_est
    """
    path = Path(path).resolve()
    
    if not path.exists() or not path.is_dir():
        return ScanResult(files_count=0, char_count=0, token_est=0)
    
    # Parse ignore patterns if present
    ignore_patterns = parse_cursorignore(path)
    
    files_count = 0
    char_count = 0
    
    for dirpath, dirnames, filenames in os.walk(path):
        current = Path(dirpath)
        
        # Filter out excluded directories (in-place)
        dirnames[:] = [
            d for d in dirnames 
            if d not in EXCLUDE_DIRS
            and not (ignore_patterns and should_ignore(current / d, path, ignore_patterns))
        ]
        
        for filename in filenames:
            file_path = current / filename
            
            # Skip if ignored by patterns
            if ignore_patterns and should_ignore(file_path, path, ignore_patterns):
                continue
            
            # Skip binary files
            ext = file_path.suffix.lower()
            if ext in BINARY_EXTENSIONS:
                continue
            
            # Try to read file
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                files_count += 1
                char_count += len(content)
            except (PermissionError, OSError, UnicodeDecodeError):
                continue
    
    return ScanResult(
        files_count=files_count,
        char_count=char_count,
        token_est=char_count // 4
    )

