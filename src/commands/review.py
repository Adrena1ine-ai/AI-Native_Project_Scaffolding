"""
Review command — generate AI code review prompt for local changes
"""

from __future__ import annotations

import subprocess
import shutil
from pathlib import Path

from ..core.constants import COLORS

# Try to import pyperclip for clipboard functionality
try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False


def get_git_diff() -> str | None:
    """
    Get git diff for current changes
    
    Returns:
        Diff string or None if no changes
    """
    if not shutil.which('git'):
        print(COLORS.error("Git is not installed"))
        return None
    
    try:
        # Get diff of staged and unstaged changes
        result = subprocess.run(
            ["git", "diff", "HEAD"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            # Try without HEAD (for new repos)
            result = subprocess.run(
                ["git", "diff"],
                capture_output=True,
                text=True,
                timeout=30
            )
        
        return result.stdout.strip() if result.stdout.strip() else None
        
    except subprocess.TimeoutExpired:
        print(COLORS.error("Git diff timed out"))
        return None
    except Exception as e:
        print(COLORS.error(f"Git error: {e}"))
        return None


def get_context_map() -> str | None:
    """
    Read CURRENT_CONTEXT_MAP.md if exists
    
    Returns:
        Content (first 2000 chars) or None
    """
    context_file = Path("CURRENT_CONTEXT_MAP.md")
    if context_file.exists():
        try:
            content = context_file.read_text(encoding="utf-8")
            return content[:2000]
        except Exception:
            pass
    return None


def get_cursor_rules() -> str | None:
    """
    Read .cursorrules if exists
    
    Returns:
        Content or None
    """
    rules_file = Path(".cursorrules")
    if rules_file.exists():
        try:
            return rules_file.read_text(encoding="utf-8")
        except Exception:
            pass
    return None


def build_review_prompt(diff: str, context: str | None, rules: str | None) -> str:
    """
    Build the review prompt for AI
    
    Args:
        diff: Git diff content
        context: Context map content (optional)
        rules: Cursor rules content (optional)
        
    Returns:
        Formatted prompt string
    """
    prompt_parts = ["[🤖 LOCAL CODE REVIEW REQUEST]", ""]
    
    # Add context if available
    if context:
        prompt_parts.extend([
            "**Project Context:**",
            context,
            ""
        ])
    
    # Add rules if available (truncated to save context)
    if rules:
        truncated_rules = rules[:1000]
        if len(rules) > 1000:
            truncated_rules += "\n... (truncated)"
        prompt_parts.extend([
            "**Project Rules (.cursorrules):**",
            truncated_rules,
            ""
        ])
    
    # Add diff
    prompt_parts.extend([
        "**My Active Changes (Git Diff):**",
        "```diff",
        diff,
        "```",
        ""
    ])
    
    # Add instructions
    prompt_parts.extend([
        "**Instructions for AI:**",
        "Act as a Senior Python Architect (CodeRabbit Profile).",
        "1. Analyze the `diff` above.",
        "2. Check for:",
        "   - 🇷🇺 Russian text (Strictly forbidden! Translate to English).",
        "   - 🐛 Logic bugs.",
        "   - 🛡️ Security issues.",
        "   - 🧹 Code style (PEP 8).",
        "3. If everything is good, just say \"✅ LGTM\".",
        "4. If issues found, use a Markdown table: | File | Line | Severity | Suggestion |",
    ])
    
    return "\n".join(prompt_parts)


def review_changes() -> bool:
    """
    Generate review prompt for current git changes
    
    Returns:
        True if prompt was generated successfully
    """
    print(f"\n{COLORS.colorize('🔍 Generating review prompt...', COLORS.CYAN)}\n")
    
    # Step A: Get diff
    diff = get_git_diff()
    if not diff:
        print(COLORS.success("No changes detected."))
        return True
    
    # Step B: Get context map
    context = get_context_map()
    if context:
        print(f"  {COLORS.success('Found CURRENT_CONTEXT_MAP.md')}")
    else:
        print(f"  {COLORS.warning('CURRENT_CONTEXT_MAP.md not found (skipping)')}")
    
    # Step C: Get cursor rules
    rules = get_cursor_rules()
    if rules:
        print(f"  {COLORS.success('Found .cursorrules')}")
    else:
        print(f"  {COLORS.warning('.cursorrules not found (skipping)')}")
    
    # Step D: Build prompt
    prompt = build_review_prompt(diff, context, rules)
    
    # Calculate stats
    diff_lines = len(diff.splitlines())
    prompt_chars = len(prompt)
    
    print(f"\n  📊 Diff: {diff_lines} lines")
    print(f"  📊 Prompt: {prompt_chars} chars (~{prompt_chars // 4} tokens)")
    
    # Copy to clipboard
    if HAS_PYPERCLIP:
        try:
            pyperclip.copy(prompt)
            print(f"\n{COLORS.success('Prompt copied to clipboard!')}")
            print(f"  📋 Paste it into Cursor Chat to start review.\n")
        except Exception as e:
            print(f"\n{COLORS.warning(f'Could not copy to clipboard: {e}')}")
            print(f"  📄 Prompt saved. Copy manually from below:\n")
            print("=" * 60)
            print(prompt)
            print("=" * 60)
    else:
        print(f"\n{COLORS.warning('pyperclip not installed. Install with: pip install pyperclip')}")
        print(f"  📄 Here's your prompt:\n")
        print("=" * 60)
        print(prompt)
        print("=" * 60)
    
    return True


def cmd_review() -> None:
    """Interactive review command"""
    print(COLORS.colorize("\n🔍 LOCAL CODE REVIEW\n", COLORS.GREEN))
    
    # Check git
    if not shutil.which('git'):
        print(COLORS.error("Git is not installed. Please install git first."))
        return
    
    # Check if in git repo
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(COLORS.error("Not in a git repository."))
        return
    
    review_changes()

