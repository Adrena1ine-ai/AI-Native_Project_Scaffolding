"""
📦 Pack — XML Context Packer
Exports project content to a single XML file for AI context sharing
"""

from __future__ import annotations

import os
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

from ..core.constants import COLORS, VERSION
from ..utils.metrics import parse_cursorignore, should_ignore, EXCLUDE_DIRS, BINARY_EXTENSIONS


# Maximum file size to include (1MB)
MAX_FILE_SIZE = 1024 * 1024

# Maximum total pack size (10MB)
MAX_PACK_SIZE = 10 * 1024 * 1024


def pack_context(
    target_path: Path,
    output_file: str = "context_dump.xml"
) -> tuple[bool, int, int]:
    """
    Pack project context into a single XML file
    
    Args:
        target_path: Path to project root
        output_file: Output filename
        
    Returns:
        Tuple of (success, files_packed, total_size)
    """
    target_path = Path(target_path).resolve()
    
    if not target_path.exists() or not target_path.is_dir():
        print(COLORS.error(f"Invalid path: {target_path}"))
        return False, 0, 0
    
    # Parse ignore patterns
    ignore_patterns = parse_cursorignore(target_path)
    
    # Collect files
    files_to_pack: list[tuple[Path, str]] = []  # (path, relative_path)
    total_size = 0
    
    for dirpath, dirnames, filenames in os.walk(target_path):
        current = Path(dirpath)
        
        # Filter directories
        dirnames[:] = [
            d for d in dirnames 
            if d not in EXCLUDE_DIRS
            and not d.startswith(".")
            and not (ignore_patterns and should_ignore(current / d, target_path, ignore_patterns))
        ]
        
        for filename in sorted(filenames):
            file_path = current / filename
            
            # Skip ignored files
            if ignore_patterns and should_ignore(file_path, target_path, ignore_patterns):
                continue
            
            # Skip binary files
            if file_path.suffix.lower() in BINARY_EXTENSIONS:
                continue
            
            # Skip hidden files
            if filename.startswith("."):
                continue
            
            # Skip output file
            if filename == output_file:
                continue
            
            # Check file size
            try:
                size = file_path.stat().st_size
                if size > MAX_FILE_SIZE:
                    continue
                if total_size + size > MAX_PACK_SIZE:
                    break
                
                rel_path = str(file_path.relative_to(target_path))
                files_to_pack.append((file_path, rel_path))
                total_size += size
                
            except OSError:
                continue
    
    # Build XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!--',
        f'  📦 AI Toolkit Context Pack v{VERSION}',
        f'  Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        f'  Project: {target_path.name}',
        f'  Files: {len(files_to_pack)}',
        '',
        '  This file contains the full project context for AI analysis.',
        '  Import this into Claude, ChatGPT, or any AI assistant.',
        '',
        '  Usage:',
        '    "Analyze this codebase: [paste XML]"',
        '    "Review the project structure and suggest improvements"',
        '-->',
        '<documents>',
    ]
    
    for file_path, rel_path in files_to_pack:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            escaped_content = escape(content)
            
            xml_lines.extend([
                f'  <document path="{escape(rel_path)}">',
                escaped_content,
                '  </document>',
            ])
        except Exception:
            continue
    
    xml_lines.append('</documents>')
    
    # Write output
    output_path = target_path / output_file
    try:
        output_path.write_text("\n".join(xml_lines), encoding="utf-8")
        return True, len(files_to_pack), total_size
    except Exception as e:
        print(COLORS.error(f"Failed to write: {e}"))
        return False, 0, 0


def cmd_pack() -> None:
    """Interactive pack command"""
    print(COLORS.colorize("\n📦 CONTEXT PACKER\n", COLORS.GREEN))
    
    # Get path
    path_str = input("  Project path [.]: ").strip() or "."
    target_path = Path(path_str).resolve()
    
    if not target_path.exists():
        print(COLORS.error("Path does not exist"))
        return
    
    # Get output file
    output_file = input("  Output file [context_dump.xml]: ").strip() or "context_dump.xml"
    
    print(f"\n  🔍 Scanning {target_path.name}...")
    
    success, files_packed, total_size = pack_context(target_path, output_file)
    
    if success:
        size_kb = total_size / 1024
        print(f"\n  {COLORS.success('Pack complete!')}")
        print(f"  📁 Files: {files_packed}")
        print(f"  📊 Size: {size_kb:.1f} KB")
        print(f"  📄 Output: {output_file}")
        print(f"\n  💡 Use: Import into any AI assistant for full context analysis\n")
    else:
        print(COLORS.error("  Pack failed"))

