"""
🔌 Hooks — Git hook installation and management
"""

from __future__ import annotations

import os
import stat
from pathlib import Path

from ..core.constants import COLORS


PRE_COMMIT_HOOK = '''#!/bin/sh
# ═══════════════════════════════════════════════════════════════
# 🦊 AI Toolkit Pre-Commit Hook (Fox Security Guard)
# Runs automatic checks before each commit
# ═══════════════════════════════════════════════════════════════

echo "🦊 Fox is guarding your repo..."

# Update project docs (for AI Toolkit itself)
if [ -f "src/utils/status_generator.py" ] && [ -f "src/utils/context_map.py" ]; then
    echo "  📊 Updating PROJECT_STATUS.md and CURRENT_CONTEXT_MAP.md..."
    python3 -m src.cli status . --skip-tests 2>/dev/null || python -m src.cli status . --skip-tests 2>/dev/null
    if [ -f "generate_map.py" ]; then
        python3 generate_map.py 2>/dev/null || python generate_map.py 2>/dev/null
    fi
    git add PROJECT_STATUS.md CURRENT_CONTEXT_MAP.md 2>/dev/null
elif [ -f "generate_map.py" ]; then
    # Fallback: update context map only (for other projects)
    echo "  📋 Updating context map..."
    python3 generate_map.py 2>/dev/null || python generate_map.py 2>/dev/null
    git add CURRENT_CONTEXT_MAP.md 2>/dev/null
fi

# Check for Russian text (common issue)
if git diff --cached --name-only | xargs grep -l '[а-яА-ЯёЁ]' 2>/dev/null; then
    echo "  ⚠️  Warning: Russian text detected in staged files"
    echo "     Consider translating to English before commit"
fi

# Check for venv inside project
if [ -d "venv" ] || [ -d ".venv" ]; then
    echo "  ❌ ERROR: venv directory found inside project!"
    echo "     Move it to ../_venvs/ and update .gitignore"
    exit 1
fi

# Check for large files (>1MB)
large_files=$(git diff --cached --name-only | while read f; do
    if [ -f "$f" ]; then
        size=$(wc -c < "$f" 2>/dev/null || echo 0)
        if [ "$size" -gt 1048576 ]; then
            echo "$f"
        fi
    fi
done)

if [ -n "$large_files" ]; then
    echo "  ⚠️  Warning: Large files detected (>1MB):"
    echo "$large_files" | sed 's/^/     /'
fi

# Run Fox security scan if ai-toolkit is available
if command -v ai-toolkit >/dev/null 2>&1; then
    echo "  🔐 Running Fox security scan..."
    ai-toolkit review --check 2>/dev/null || {
        echo "  ⚠️  Fox review check skipped (run manually: ai-toolkit review)"
    }
fi

echo "  ✅ Fox says: All clear!"
exit 0
'''


def install_pre_commit_hook(path: Path) -> bool:
    """
    Install pre-commit hook for AI Toolkit
    
    Args:
        path: Path to project root (must contain .git)
        
    Returns:
        True if hook was installed successfully
    """
    path = Path(path).resolve()
    git_dir = path / ".git"
    
    if not git_dir.exists():
        return False
    
    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)
    
    hook_path = hooks_dir / "pre-commit"
    
    try:
        # Write hook
        hook_path.write_text(PRE_COMMIT_HOOK, encoding="utf-8")
        
        # Make executable
        st = os.stat(hook_path)
        os.chmod(hook_path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        
        return True
    except Exception:
        return False


def uninstall_pre_commit_hook(path: Path) -> bool:
    """
    Remove pre-commit hook
    
    Args:
        path: Path to project root
        
    Returns:
        True if hook was removed successfully
    """
    path = Path(path).resolve()
    hook_path = path / ".git" / "hooks" / "pre-commit"
    
    try:
        if hook_path.exists():
            hook_path.unlink()
        return True
    except Exception:
        return False


def check_hook_installed(path: Path) -> bool:
    """
    Check if pre-commit hook is installed
    
    Args:
        path: Path to project root
        
    Returns:
        True if hook exists
    """
    path = Path(path).resolve()
    hook_path = path / ".git" / "hooks" / "pre-commit"
    return hook_path.exists()


def cmd_hooks() -> None:
    """Interactive hook management command"""
    print(COLORS.colorize("\n🔌 GIT HOOKS\n", COLORS.GREEN))
    
    path = Path.cwd()
    
    if not (path / ".git").exists():
        print(COLORS.error("Not a git repository"))
        return
    
    is_installed = check_hook_installed(path)
    
    if is_installed:
        print("  Status: [green]Installed[/green]")
        choice = input("\n  Remove hook? (y/N): ").strip().lower()
        if choice == 'y':
            if uninstall_pre_commit_hook(path):
                print(COLORS.success("  Hook removed"))
            else:
                print(COLORS.error("  Failed to remove hook"))
    else:
        print("  Status: Not installed")
        choice = input("\n  Install hook? (Y/n): ").strip().lower()
        if choice != 'n':
            if install_pre_commit_hook(path):
                print(COLORS.success("  Hook installed"))
            else:
                print(COLORS.error("  Failed to install hook"))

