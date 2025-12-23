"""
Auto-generate PROJECT_STATUS.md from actual codebase state.
Scans commands, utilities, generators, and tests to build accurate status.
"""

from __future__ import annotations

import ast
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional


def scan_commands(src_path: Path) -> List[Dict[str, str]]:
    """
    Scan src/commands/ and return list of implemented commands.
    Parses AST to find cmd_* functions and their docstrings.
    """
    commands = []
    commands_dir = src_path / "commands"
    
    if not commands_dir.exists():
        return commands
    
    for py_file in commands_dir.glob("*.py"):
        if py_file.name.startswith("_"):
            continue
        
        try:
            content = py_file.read_text(encoding="utf-8")
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith("cmd_"):
                    cmd_name = node.name.replace("cmd_", "")
                    docstring = ast.get_docstring(node) or "No description"
                    commands.append({
                        "name": cmd_name,
                        "file": py_file.name,
                        "description": docstring.split("\n")[0]
                    })
        except SyntaxError:
            continue
    
    return commands


def scan_utilities(src_path: Path) -> List[Dict[str, str]]:
    """Scan src/utils/ for utility modules."""
    utils = []
    utils_dir = src_path / "utils"
    
    if not utils_dir.exists():
        return utils
    
    for py_file in utils_dir.glob("*.py"):
        if py_file.name.startswith("_"):
            continue
        
        try:
            content = py_file.read_text(encoding="utf-8")
            tree = ast.parse(content)
            module_doc = ast.get_docstring(tree) or py_file.stem.replace("_", " ").title()
            
            utils.append({
                "name": py_file.stem,
                "file": f"src/utils/{py_file.name}",
                "description": module_doc.split("\n")[0]
            })
        except SyntaxError:
            continue
    
    return utils


def scan_generators(src_path: Path) -> List[Dict[str, str]]:
    """Scan src/generators/ for generator modules."""
    generators = []
    gen_dir = src_path / "generators"
    
    if not gen_dir.exists():
        return generators
    
    for py_file in gen_dir.glob("*.py"):
        if py_file.name.startswith("_"):
            continue
        
        try:
            content = py_file.read_text(encoding="utf-8")
            tree = ast.parse(content)
            module_doc = ast.get_docstring(tree) or py_file.stem.replace("_", " ").title()
            
            generators.append({
                "name": py_file.stem,
                "file": f"src/generators/{py_file.name}",
                "description": module_doc.split("\n")[0]
            })
        except SyntaxError:
            continue
    
    return generators


def run_tests(project_root: Path) -> Tuple[int, int]:
    """Run pytest and return (passed, total)."""
    try:
        result = subprocess.run(
            ["pytest", "tests/", "-v", "--tb=no", "-q"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=project_root
        )
        
        output = result.stdout + result.stderr
        
        # Parse "X passed" or "X passed, Y failed"
        for line in output.split("\n"):
            if "passed" in line:
                match = re.search(r"(\d+)\s+passed", line)
                if match:
                    passed = int(match.group(1))
                    # Check for failed
                    failed_match = re.search(r"(\d+)\s+failed", line)
                    failed = int(failed_match.group(1)) if failed_match else 0
                    return passed, passed + failed
        
        return 0, 0
    except Exception:
        return 0, 0


def check_file_exists(project_root: Path, filepath: str) -> bool:
    """Check if a file exists in project."""
    return (project_root / filepath).exists()


def get_version(project_root: Path) -> str:
    """Get current version from constants.py."""
    constants_file = project_root / "src" / "core" / "constants.py"
    if constants_file.exists():
        content = constants_file.read_text(encoding="utf-8")
        for line in content.split("\n"):
            if "VERSION" in line and "=" in line and not line.strip().startswith("#"):
                # Extract version string
                try:
                    version = line.split("=")[1].strip().strip('"\'')
                    return version
                except IndexError:
                    continue
    return "3.3"


def generate_status_md(project_root: Path, skip_tests: bool = False) -> str:
    """
    Generate complete PROJECT_STATUS.md content.
    
    Args:
        project_root: Path to project root
        skip_tests: If True, don't run pytest (faster)
    """
    src_path = project_root / "src"
    version = get_version(project_root)
    
    commands = scan_commands(src_path)
    utilities = scan_utilities(src_path)
    generators = scan_generators(src_path)
    
    if skip_tests:
        passed, total = 0, 0
        test_status = "Skipped (use --run-tests to include)"
    else:
        passed, total = run_tests(project_root)
        if total > 0:
            test_status = f"{passed}/{total} passed ({int(passed/total*100)}%)"
        else:
            test_status = "No tests found or pytest not available"
    
    # Build markdown
    lines = [
        f"# 📊 Project Status — AI Toolkit v{version}",
        "",
        "> ⚡ Auto-generated from codebase. Do not edit manually.",
        f"> 🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        "## ✅ Implemented Commands",
        "",
    ]
    
    # Commands table
    if commands:
        lines.append("| Command | Description |")
        lines.append("|---------|-------------|")
        for cmd in sorted(commands, key=lambda x: x["name"]):
            lines.append(f"| `{cmd['name']}` | {cmd['description']} |")
    else:
        lines.append("_No commands found_")
    
    lines.extend([
        "",
        "---",
        "",
        "## 🛠️ Utilities",
        "",
    ])
    
    for util in utilities:
        lines.append(f"- [x] `{util['file']}` — {util['description']}")
    
    if not utilities:
        lines.append("_No utilities found_")
    
    lines.extend([
        "",
        "---",
        "",
        "## 🏭 Generators",
        "",
    ])
    
    for gen in generators:
        lines.append(f"- [x] `{gen['file']}` — {gen['description']}")
    
    if not generators:
        lines.append("_No generators found_")
    
    lines.extend([
        "",
        "---",
        "",
        "## 📁 Documentation Status",
        "",
    ])
    
    docs = [
        ("README.md", "Project overview"),
        ("PROMPTS_LIBRARY.md", "Curated prompts for AI"),
        ("TRADEOFFS.md", "Architectural decisions"),
        ("CLAUDE.md", "Claude AI instructions"),
        ("CONTRIBUTING.md", "Contribution guide"),
        ("_AI_INCLUDE/WHERE_THINGS_LIVE.md", "Location guide"),
        ("_AI_INCLUDE/PROJECT_CONVENTIONS.md", "Project conventions"),
        (".cursor/rules/project.md", "Cursor project rules"),
        (".cursor/rules/toolkit.md", "Cursor toolkit rules"),
        ("docs/QUICK_START.md", "Quick start guide"),
        ("docs/FAQ.md", "Frequently asked questions"),
    ]
    
    lines.append("| Document | Status |")
    lines.append("|----------|--------|")
    for doc_path, desc in docs:
        exists = check_file_exists(project_root, doc_path)
        status = "✅" if exists else "❌"
        lines.append(f"| `{doc_path}` | {status} {desc} |")
    
    lines.extend([
        "",
        "---",
        "",
        "## 📈 Test Coverage",
        "",
        "```",
        f"Tests: {test_status}",
        "```",
        "",
        "---",
        "",
        "## 📊 Quick Stats",
        "",
        f"- **Commands:** {len(commands)}",
        f"- **Utilities:** {len(utilities)}",
        f"- **Generators:** {len(generators)}",
        f"- **Version:** {version}",
        "",
        "---",
        "",
        "## 🔗 Quick Links",
        "",
        "| Document | Purpose |",
        "|----------|---------|",
        "| `TECHNICAL_SPECIFICATION.md` | Roadmap (Strategy) |",
        "| `_AI_INCLUDE/WHERE_THINGS_LIVE.md` | Rules (Tactics) |",
        "| `CURRENT_CONTEXT_MAP.md` | Auto-generated structure |",
        "| `.cursor/rules/project.md` | Constitution |",
        "",
        "---",
        "",
        f"*Auto-generated by AI Toolkit v{version} — Status Generator*",
    ])
    
    return "\n".join(lines)


def update_status(project_root: Path, skip_tests: bool = False) -> Path:
    """
    Generate and write PROJECT_STATUS.md.
    
    Returns:
        Path to the generated file
    """
    content = generate_status_md(project_root, skip_tests=skip_tests)
    status_file = project_root / "PROJECT_STATUS.md"
    status_file.write_text(content, encoding="utf-8")
    return status_file

