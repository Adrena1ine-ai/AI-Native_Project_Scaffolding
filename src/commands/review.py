"""
🦊 Fox — Security Scanner & Code Review Prompt Generator
Evolved from Rabbit: Now focuses on security (secrets detection) instead of language checks
"""

from __future__ import annotations

import re
import subprocess
import shutil
import math
from pathlib import Path
from dataclasses import dataclass

from ..core.constants import COLORS

# Try to import pyperclip for clipboard functionality
try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False


# ═══════════════════════════════════════════════════════════════
# SECRET DETECTION PATTERNS
# ═══════════════════════════════════════════════════════════════

SECRET_PATTERNS = [
    # OpenAI API Keys
    (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API Key"),
    
    # Telegram Bot Tokens
    (r'\b\d{8,10}:[A-Za-z0-9_-]{35,}\b', "Telegram Bot Token"),
    
    # AWS Keys
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key ID"),
    (r'(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])', "Possible AWS Secret Key"),
    
    # GitHub Tokens
    (r'ghp_[a-zA-Z0-9]{36}', "GitHub Personal Access Token"),
    (r'gho_[a-zA-Z0-9]{36}', "GitHub OAuth Token"),
    (r'ghs_[a-zA-Z0-9]{36}', "GitHub Server Token"),
    
    # Generic high-entropy secrets in assignments
    (r'(?:api_?key|apikey|secret|token|password|passwd|pwd)\s*[=:]\s*["\'][a-zA-Z0-9+/=_-]{20,}["\']', "Generic Secret Assignment"),
]

# Patterns to exclude (placeholders)
PLACEHOLDER_PATTERNS = [
    r'your[_-]?key[_-]?here',
    r'your[_-]?token[_-]?here',
    r'your[_-]?secret[_-]?here',
    r'xxx+',
    r'placeholder',
    r'example',
    r'test[_-]?key',
    r'dummy',
    r'sample',
    r'<[^>]+>',  # <YOUR_KEY_HERE>
]


@dataclass
class SecretFinding:
    """A detected secret"""
    file_path: str
    line_number: int
    secret_type: str
    snippet: str  # Redacted snippet


def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy of a string"""
    if not text:
        return 0.0
    
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    
    entropy = 0.0
    for count in freq.values():
        p = count / len(text)
        entropy -= p * math.log2(p)
    
    return entropy


def is_placeholder(value: str) -> bool:
    """Check if a value is a placeholder, not a real secret"""
    value_lower = value.lower()
    
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, value_lower, re.IGNORECASE):
            return True
    
    # Low entropy strings are likely placeholders
    if calculate_entropy(value) < 3.0 and len(value) < 30:
        return True
    
    return False


def check_secrets(content: str, file_path: str = "") -> list[SecretFinding]:
    """
    Scan content for potential secrets
    
    Args:
        content: File content to scan
        file_path: Path for reporting
        
    Returns:
        List of SecretFinding objects
    """
    findings = []
    lines = content.splitlines()
    
    for line_num, line in enumerate(lines, 1):
        # Skip comments that look like documentation
        stripped = line.strip()
        if stripped.startswith("#") and ("example" in stripped.lower() or "e.g." in stripped.lower()):
            continue
        
        for pattern, secret_type in SECRET_PATTERNS:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            
            for match in matches:
                matched_text = match.group(0)
                
                # Skip placeholders
                if is_placeholder(matched_text):
                    continue
                
                # Skip if it's in a comment explaining format
                if "format:" in line.lower() or "example:" in line.lower():
                    continue
                
                # Create redacted snippet
                if len(matched_text) > 10:
                    snippet = matched_text[:4] + "***" + matched_text[-4:]
                else:
                    snippet = "***"
                
                findings.append(SecretFinding(
                    file_path=file_path,
                    line_number=line_num,
                    secret_type=secret_type,
                    snippet=snippet
                ))
    
    return findings


def run_fox_scan(project_path: Path) -> tuple[bool, list[SecretFinding]]:
    """
    Run the Fox security scanner on a project
    
    Args:
        project_path: Path to project root
        
    Returns:
        Tuple of (passed, findings)
    """
    findings = []
    
    # Get files to scan (Python files, not ignored)
    try:
        for py_file in project_path.rglob("*.py"):
            # Skip virtual envs and caches
            path_str = str(py_file)
            if any(skip in path_str for skip in ["venv", ".venv", "__pycache__", "_AI_ARCHIVE", "site-packages"]):
                continue
            
            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
                rel_path = str(py_file.relative_to(project_path))
                file_findings = check_secrets(content, rel_path)
                findings.extend(file_findings)
            except Exception:
                continue
    except Exception:
        pass
    
    return len(findings) == 0, findings


# ═══════════════════════════════════════════════════════════════
# GIT DIFF & PROMPT GENERATION
# ═══════════════════════════════════════════════════════════════

def get_git_diff() -> str | None:
    """Get git diff for current changes"""
    if not shutil.which('git'):
        print(COLORS.error("Git is not installed"))
        return None
    
    try:
        result = subprocess.run(
            ["git", "diff", "HEAD"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
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
    """Read CURRENT_CONTEXT_MAP.md if exists"""
    context_file = Path("CURRENT_CONTEXT_MAP.md")
    if context_file.exists():
        try:
            content = context_file.read_text(encoding="utf-8")
            return content[:2000]
        except Exception:
            pass
    return None


def get_cursor_rules() -> str | None:
    """Read .cursorrules if exists"""
    rules_file = Path(".cursorrules")
    if rules_file.exists():
        try:
            return rules_file.read_text(encoding="utf-8")
        except Exception:
            pass
    return None


def build_review_prompt(diff: str, context: str | None, rules: str | None) -> str:
    """Build the review prompt for AI"""
    prompt_parts = ["[🦊 FOX CODE REVIEW REQUEST]", ""]
    
    # Add context if available
    if context:
        prompt_parts.extend([
            "**Project Context:**",
            context,
            ""
        ])
    
    # Add rules if available (truncated)
    if rules:
        truncated_rules = rules[:1000]
        if len(rules) > 1000:
            truncated_rules += "\n... (truncated)"
        prompt_parts.extend([
            "**Project Rules:**",
            truncated_rules,
            ""
        ])
    
    # Add diff
    prompt_parts.extend([
        "**Changes (Git Diff):**",
        "```diff",
        diff,
        "```",
        ""
    ])
    
    # Updated instructions (no Russian check)
    prompt_parts.extend([
        "**Instructions for AI:**",
        "Act as a Senior Python Architect.",
        "1. Analyze the `diff` above.",
        "2. Check for:",
        "   - 🔐 Hardcoded secrets (API keys, tokens, passwords).",
        "   - 🐛 Logic bugs and edge cases.",
        "   - 🛡️ Security vulnerabilities.",
        "   - 🧹 Code style (PEP 8, type hints).",
        "3. If everything is good, say \"✅ LGTM\".",
        "4. If issues found, use: | File | Line | Severity | Suggestion |",
    ])
    
    return "\n".join(prompt_parts)


def review_changes() -> bool:
    """Generate review prompt for current git changes"""
    print(f"\n{COLORS.colorize('🦊 Fox Security Scanner & Review', COLORS.CYAN)}\n")
    
    # Step 1: Get diff
    diff = get_git_diff()
    if not diff:
        print(COLORS.success("No changes detected."))
        return True
    
    # Step 2: Security scan on diff content
    print("  🔍 Scanning for secrets...")
    diff_findings = check_secrets(diff, "git diff")
    
    if diff_findings:
        print(f"\n  {COLORS.error(f'🚨 SECRETS DETECTED! ({len(diff_findings)} found)')}\n")
        for finding in diff_findings[:5]:
            print(f"    ⚠️  Line {finding.line_number}: {finding.secret_type}")
            print(f"       Snippet: {finding.snippet}")
        if len(diff_findings) > 5:
            print(f"    ... and {len(diff_findings) - 5} more")
        print(f"\n  {COLORS.error('Remove secrets before committing!')}\n")
        return False
    
    print(f"  {COLORS.success('No secrets detected')}")
    
    # Step 3: Get context
    context = get_context_map()
    rules = get_cursor_rules()
    
    # Step 4: Build prompt
    prompt = build_review_prompt(diff, context, rules)
    
    # Stats
    diff_lines = len(diff.splitlines())
    prompt_chars = len(prompt)
    
    print(f"\n  📊 Diff: {diff_lines} lines")
    print(f"  📊 Prompt: {prompt_chars} chars (~{prompt_chars // 4} tokens)")
    
    # Copy to clipboard
    if HAS_PYPERCLIP:
        try:
            pyperclip.copy(prompt)
            print(f"\n{COLORS.success('Prompt copied to clipboard!')}")
            print(f"  📋 Paste into Cursor Chat for review.\n")
        except Exception as e:
            print(f"\n{COLORS.warning(f'Clipboard error: {e}')}")
            _print_prompt(prompt)
    else:
        print(f"\n{COLORS.warning('pyperclip not installed')}")
        _print_prompt(prompt)
    
    return True


def _print_prompt(prompt: str) -> None:
    """Print prompt to console"""
    print("=" * 60)
    print(prompt)
    print("=" * 60)


def cmd_review() -> None:
    """Interactive review command (Fox)"""
    print(COLORS.colorize("\n🦊 FOX SECURITY REVIEW\n", COLORS.GREEN))
    
    if not shutil.which('git'):
        print(COLORS.error("Git is not installed."))
        return
    
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(COLORS.error("Not in a git repository."))
        return
    
    review_changes()
