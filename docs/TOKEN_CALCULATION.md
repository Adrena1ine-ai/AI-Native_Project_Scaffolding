# 📊 Token Calculation in AI Toolkit Doctor

## Overview

The Doctor command calculates token consumption to help you understand which files are consuming the most context window space when working with AI assistants like Cursor, GitHub Copilot, or Claude.

## How Tokens Are Calculated

### Formula

```python
tokens = file_content_length_in_characters / 4
```

This is a **rough approximation** based on the industry standard that:
- 1 token ≈ 4 characters (for English text)
- 1 token ≈ 0.75 words (on average)

### Example

```python
# File: main.py (200 characters)
print("Hello World")
def main():
    pass

# Token estimate: 200 / 4 = 50 tokens
```

## What Files Are Counted?

The Doctor scans these file types:
- `*.py` — Python source files
- `*.md` — Markdown documentation
- `*.txt` — Text files
- `*.json` — JSON configuration
- `*.yaml`, `*.yml` — YAML configuration
- `*.toml` — TOML configuration

### Excluded Directories

These are **automatically excluded** from token counting:
- `venv/`, `.venv/`, `env/` — Virtual environments
- `node_modules/` — Node.js dependencies
- `__pycache__/` — Python cache
- `.git/` — Git repository data

## Token Breakdown Display

### Main Report (Top 5)

```
╠══════════════════════════════════════════════════════════════════╣
║  📊 TOP TOKEN CONSUMERS (>1K tokens)                             ║
║  • src/commands/doctor.py — 8.8K                                  ║
║  • src/commands/wizard.py — 6.7K                                  ║
║  • src/commands/trace.py — 3.6K                                   ║
║  • benchmark.py — 3.6K                                            ║
║  • first manifesto.md — 3.6K                                      ║
║  ... and 5 more files >1K tokens                                ║
╠══════════════════════════════════════════════════════════════════╣
```

### Full Breakdown ([T] option)

Press `T` in interactive mode to see:

1. **All files >1000 tokens** (up to top 20)
   - Exact token count per file
   - Relative path from project root

2. **Breakdown by file type**
   - Total tokens per extension
   - File count per extension

Example:

```
╔══════════════════════════════════════════════════════════════════╗
║  📊 DETAILED TOKEN BREAKDOWN                                     ║
╠══════════════════════════════════════════════════════════════════╣
║  Total: 115.4K tokens across 79 files                            ║
╠══════════════════════════════════════════════════════════════════╣
║  FILES WITH >1000 TOKENS:                                        ║
║                                                                  ║
║    8,838 — src/commands/doctor.py                                ║
║    6,677 — src/commands/wizard.py                                ║
║    3,636 — src/commands/trace.py                                 ║
║  ... (more files)                                                ║
╠══════════════════════════════════════════════════════════════════╣
║  BREAKDOWN BY FILE TYPE:                                         ║
║                                                                  ║
║  .py           80.4K (51 files)                                  ║
║  .md           33.8K (25 files)                                  ║
║  .toml          1.1K (1 files)                                   ║
╚══════════════════════════════════════════════════════════════════╝
```

## Why This Matters

### Context Window Limits

Different AI assistants have different context window limits:

| AI Assistant | Context Window | Approximate Files |
|--------------|----------------|-------------------|
| GPT-4 | 8K tokens | ~8-10 medium files |
| GPT-4 Turbo | 128K tokens | ~100+ files |
| Claude 3 | 200K tokens | ~150+ files |
| Claude 3.5 Sonnet | 200K tokens | ~150+ files |

### Token Thresholds

The Doctor uses these thresholds:

- **< 100K tokens** — 🟢 OK (healthy project)
- **100K - 1M tokens** — 🟡 HIGH (consider optimization)
- **> 1M tokens** — 🔴 CRITICAL (AI will struggle)

## Optimization Strategies

### 1. Move Large Files

Files >1000 tokens that aren't frequently edited:

```bash
# Move to external location
mkdir -p ../_data/my_project
mv large_dataset.json ../_data/my_project/
```

### 2. Use .cursorignore

Exclude files from AI indexing:

```gitignore
# .cursorignore
logs/
*.log
data/
*.csv
*.db
docs/archive/
```

### 3. Split Large Files

If a single file has >5000 tokens, consider splitting:

```python
# Before: handlers.py (8000 tokens)
# All handlers in one file

# After: Split into modules
handlers/
  __init__.py
  start.py      (1500 tokens)
  settings.py   (1200 tokens)
  admin.py      (2000 tokens)
```

## Programmatic Access

### Python API

```python
from pathlib import Path
from src.commands.doctor import Doctor, print_token_breakdown

# Create doctor instance
doctor = Doctor(Path("/path/to/project"))

# Run diagnosis
report = doctor.diagnose()

# Access token data
print(f"Total tokens: {report.total_tokens}")
print(f"Files scanned: {len(report.file_tokens)}")

# Get high-token files
for file in report.high_token_files[:10]:
    print(f"{file.relative_path}: {file.tokens} tokens")

# Show full breakdown
print_token_breakdown(report)
```

### CLI Usage

```bash
# Basic report
python main.py doctor /path/to/project --report

# Interactive mode (press T for breakdown)
python main.py doctor /path/to/project

# Auto-fix with token report
python main.py doctor /path/to/project --auto
```

## Technical Details

### Token Estimation Accuracy

The 4-character-per-token rule is an approximation:

**More accurate for:**
- English prose
- Python code with standard naming
- Markdown documentation

**Less accurate for:**
- Non-English text (e.g., Chinese: ~1.5 chars/token)
- Heavily compressed code
- JSON with long strings

**Typical variance:** ±20% from actual tokenizer

### Performance

Token calculation is **fast** because:
- Uses simple character counting (no tokenizer)
- Reads files once during diagnosis
- Caches results in `DiagnosticReport`

**Benchmark:**
- 100 files: ~0.1 seconds
- 1000 files: ~1 second
- 10,000 files: ~10 seconds

## FAQ

### Q: Why not use the actual tokenizer?

**A:** Speed and simplicity. The 4-char approximation is:
- 100x faster than running tiktoken/transformers
- Good enough for optimization decisions
- Doesn't require external dependencies

### Q: What if my project has >1M tokens?

**A:** The Doctor will flag this as CRITICAL. Solutions:
1. Use `.cursorignore` aggressively
2. Move data files to `../_data/`
3. Archive old code to `_AI_ARCHIVE/`
4. Split monolithic files

### Q: Do tokens include whitespace?

**A:** Yes, all characters count (including spaces, tabs, newlines).

### Q: Can I exclude specific files from token counting?

**A:** Yes, use `.cursorignore`. Files matching patterns won't be counted.

## See Also

- [Doctor Command Documentation](DOCTOR_COMMAND.md)
- [Project Optimization Guide](OPTIMIZATION.md)
- [.cursorignore Best Practices](CURSORIGNORE.md)

