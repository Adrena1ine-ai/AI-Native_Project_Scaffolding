"""
Manifesto Parser - Load and apply rules from manifesto.md

Manifesto is the project's "Constitution", defining:
- Project structure
- Exclusion files
- Protective scripts
- Rules for AI assistants
"""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
import re


# Path to manifesto
MANIFESTO_PATH = Path(__file__).parent.parent.parent / "AI-Native Project Scaffolding" / "manifesto.md"
MANIFESTO_BACKUP = Path(__file__).parent.parent.parent / "docs" / "manifesto.md"


@dataclass
class ManifestoRules:
    """Rules extracted from manifesto.md"""
    
    # Project structure
    recommended_folders: list[str] = field(default_factory=list)
    external_folders: list[str] = field(default_factory=list)
    
    # Exclusion files
    cursorignore_content: str = ""
    gitignore_content: str = ""
    vscode_settings: str = ""
    project_conventions: str = ""
    
    # Scripts
    bootstrap_script: str = ""
    check_repo_script: str = ""
    
    # AI Prompt
    ai_prompt: str = ""
    
    # Main rules (3 prohibitions)
    main_rules: list[str] = field(default_factory=list)


def load_manifesto(path: Optional[Path] = None) -> str:
    """
    Load manifesto.md content
    
    Args:
        path: Path to file (or None for auto-search)
        
    Returns:
        File content
    """
    if path and path.exists():
        return path.read_text(encoding="utf-8")
    
    # Try main path
    if MANIFESTO_PATH.exists():
        return MANIFESTO_PATH.read_text(encoding="utf-8")
    
    # Try backup path
    if MANIFESTO_BACKUP.exists():
        return MANIFESTO_BACKUP.read_text(encoding="utf-8")
    
    return ""


def extract_code_block(content: str, marker: str) -> str:
    """
    Extract code block content after a specific marker
    
    Args:
        content: Full manifesto text
        marker: Header text before block (e.g. "### `.cursorignore`")
        
    Returns:
        Code block content
    """
    # Find the marker
    idx = content.find(marker)
    if idx == -1:
        return ""
    
    # Find the next code block after marker
    after_marker = content[idx + len(marker):]
    
    # Match ```...``` block
    match = re.search(r'```\w*\n(.*?)```', after_marker, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    return ""


def parse_manifesto(content: str) -> ManifestoRules:
    """
    Parse manifesto.md and extract rules
    
    Args:
        content: Manifesto.md content
        
    Returns:
        ManifestoRules with extracted rules
    """
    rules = ManifestoRules()
    
    if not content:
        return rules
    
    # Main rules (from text)
    rules.main_rules = [
        "Never create venv inside project",
        "Store logs and data outside repository",
        "Use exclusion files for AI and Git",
    ]
    
    # Recommended project folders
    rules.recommended_folders = [
        "handlers/",
        "utils/",
        "api/",
        "webapp/",
        "parser/",
        "database/",
        "scripts/",
        "_AI_INCLUDE/",
        ".vscode/",
    ]
    
    # External folders (outside project)
    rules.external_folders = [
        "../_venvs/{project}-main",
        "../_data/{project}/",
        "../_artifacts/{project}/logs/",
        "../_pw-browsers/",
    ]
    
    # Extract exclusion files
    rules.cursorignore_content = extract_code_block(content, "### `.cursorignore`")
    rules.gitignore_content = extract_code_block(content, "### `.gitignore`")
    rules.vscode_settings = extract_code_block(content, "### `.vscode/settings.json`")
    rules.project_conventions = extract_code_block(content, "### `_AI_INCLUDE/PROJECT_CONVENTIONS.md`")
    
    # Extract scripts
    rules.bootstrap_script = extract_code_block(content, "### `scripts/bootstrap.sh`")
    rules.check_repo_script = extract_code_block(content, "### `scripts/check_repo_clean.sh`")
    
    # AI Prompt
    ai_prompt_marker = "## 4) Universal Prompt"
    idx = content.find(ai_prompt_marker)
    if idx != -1:
        after = content[idx:]
        match = re.search(r'```text\n(.*?)```', after, re.DOTALL)
        if match:
            rules.ai_prompt = match.group(1).strip()
    
    return rules


def get_manifesto_rules() -> ManifestoRules:
    """
    Get rules from manifesto (main function)
    
    Returns:
        ManifestoRules with rules
    """
    content = load_manifesto()
    return parse_manifesto(content)


def get_cursorignore_content() -> str:
    """Get .cursorignore content from manifesto"""
    rules = get_manifesto_rules()
    return rules.cursorignore_content or DEFAULT_CURSORIGNORE


def get_gitignore_content() -> str:
    """Get .gitignore content from manifesto"""
    rules = get_manifesto_rules()
    return rules.gitignore_content or DEFAULT_GITIGNORE


def get_bootstrap_script() -> str:
    """Get bootstrap.sh script from manifesto"""
    rules = get_manifesto_rules()
    return rules.bootstrap_script or DEFAULT_BOOTSTRAP


# Default values if manifesto is unavailable
DEFAULT_CURSORIGNORE = """# Environments / deps
venv/
.venv/
**/.venv*/
**/site-packages/

# Python caches
**/__pycache__/
**/*.pyc
**/*.pyo

# Logs
logs/
*.log

# Frontend deps/build
node_modules/
dist/
build/
.next/

# Heavy artifacts/data
**/*.csv
**/*.jsonl
**/*.db
**/*.sqlite
**/*.sqlite3

# Playwright
**/playwright/driver/
"""

DEFAULT_GITIGNORE = """# Envs
venv/
.venv/
**/.venv*/
**/site-packages/

# Caches
**/__pycache__/
**/*.pyc
**/*.pyo
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Logs
logs/
*.log

# Frontend
node_modules/
dist/
build/
.next/

# Secrets
.env

# Data/artifacts
*.csv
*.jsonl
*.db
*.sqlite
*.sqlite3
"""

DEFAULT_BOOTSTRAP = """#!/usr/bin/env bash
set -euo pipefail

PROJ="$(basename "$PWD")"
VENV_DIR="../_venvs/${PROJ}-main"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python -m pip install -U pip wheel

if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi

echo "Activate: source $VENV_DIR/bin/activate"
"""


def apply_manifesto_to_project(project_path: Path) -> dict[str, bool]:
    """
    Apply manifesto rules to an existing project
    
    Args:
        project_path: Path to project
        
    Returns:
        Dictionary with results {file: success}
    """
    results = {}
    rules = get_manifesto_rules()
    
    # Create .cursorignore
    cursorignore = project_path / ".cursorignore"
    if not cursorignore.exists():
        cursorignore.write_text(rules.cursorignore_content or DEFAULT_CURSORIGNORE, encoding="utf-8")
        results[".cursorignore"] = True
    else:
        results[".cursorignore"] = False  # Already exists
    
    # Create .gitignore
    gitignore = project_path / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(rules.gitignore_content or DEFAULT_GITIGNORE, encoding="utf-8")
        results[".gitignore"] = True
    else:
        results[".gitignore"] = False
    
    # Create .vscode/settings.json
    vscode_dir = project_path / ".vscode"
    vscode_dir.mkdir(exist_ok=True)
    vscode_settings = vscode_dir / "settings.json"
    if not vscode_settings.exists() and rules.vscode_settings:
        vscode_settings.write_text(rules.vscode_settings, encoding="utf-8")
        results[".vscode/settings.json"] = True
    else:
        results[".vscode/settings.json"] = False
    
    # Create _AI_INCLUDE/PROJECT_CONVENTIONS.md
    ai_include_dir = project_path / "_AI_INCLUDE"
    ai_include_dir.mkdir(exist_ok=True)
    conventions = ai_include_dir / "PROJECT_CONVENTIONS.md"
    if not conventions.exists() and rules.project_conventions:
        conventions.write_text(rules.project_conventions, encoding="utf-8")
        results["_AI_INCLUDE/PROJECT_CONVENTIONS.md"] = True
    else:
        results["_AI_INCLUDE/PROJECT_CONVENTIONS.md"] = False
    
    # Create scripts/bootstrap.sh
    scripts_dir = project_path / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    bootstrap = scripts_dir / "bootstrap.sh"
    if not bootstrap.exists():
        bootstrap.write_text(rules.bootstrap_script or DEFAULT_BOOTSTRAP, encoding="utf-8")
        bootstrap.chmod(bootstrap.stat().st_mode | 0o111)  # Make executable
        results["scripts/bootstrap.sh"] = True
    else:
        results["scripts/bootstrap.sh"] = False
    
    return results
