# 🔍 Code Review Guidelines

## Review Command (`src/commands/review.py`)

The `review` command generates an AI code review prompt from local Git changes.

### How It Works

1. **Get Git Diff** — `git diff HEAD` to capture staged + unstaged changes
2. **Get Context Map** — Read first 2000 chars of `CURRENT_CONTEXT_MAP.md`
3. **Get Cursor Rules** — Read first 1000 chars of `.cursorrules`
4. **Build Prompt** — Assemble structured review request
5. **Copy to Clipboard** — Using `pyperclip` if available

### Review Checklist

When reviewing code for this project, check:

| Category | Check |
|----------|-------|
| 🇷🇺 **Language** | NO Russian text anywhere (comments, strings, docstrings) |
| 🐛 **Logic** | Correct control flow, edge cases handled |
| 🛡️ **Security** | No hardcoded secrets, proper input validation |
| 🧹 **Style** | PEP 8, type hints, docstrings |
| 📦 **Imports** | No unused imports, correct relative imports |
| 🔄 **DRY** | No code duplication |

### Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 **Critical** | Security issue, data loss risk | Block merge |
| 🟠 **Major** | Logic bug, missing validation | Should fix |
| 🟡 **Minor** | Style issue, optimization | Nice to have |
| 🟢 **Info** | Suggestion, best practice | Optional |

### Output Format

When issues are found, use this table format:

```markdown
| File | Line | Severity | Suggestion |
|------|------|----------|------------|
| src/cli.py | 45 | 🟠 Major | Missing error handling for invalid input |
```

### LGTM Response

If code is clean:
```
✅ LGTM — Code looks good, no issues found.
```

