# 🏥 Doctor Command — Complete Guide

## Overview

The Doctor command is a comprehensive diagnostic and auto-fix tool that analyzes your project for AI optimization issues and provides one-click fixes.

## Quick Start

```bash
# Interactive diagnosis
python main.py doctor /path/to/project

# Report only (no fixes)
python main.py doctor /path/to/project --report

# Auto-fix everything
python main.py doctor /path/to/project --auto
```

## Features

### 1. Issue Detection

The Doctor detects these issues:

#### 🔴 CRITICAL
- **venv inside project** — Virtual environments consuming massive tokens
- **node_modules inside project** — Should be in .cursorignore

#### 🟡 WARNING
- **__pycache__ directories** — Python cache consuming tokens
- **logs/ folder** — Log files that should be archived
- **Scattered .log files** — Should be cleaned up
- **Large data files (>1MB)** — Should be moved to `../_data/`

#### 🟢 SUGGESTION
- **Missing _AI_INCLUDE/** — Project conventions not defined
- **Missing .cursorignore** — AI will index everything
- **Missing bootstrap scripts** — No setup automation
- **No virtual environment** — Expected in `../_venvs/`

### 2. Token Analysis

Shows which files consume the most context window space:

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

Press **[T]** for full breakdown with:
- All files >1000 tokens
- Breakdown by file type (.py, .md, etc.)
- Total token count across project

### 3. Auto-Fix Actions

Each issue has an automatic fix:

| Issue | Fix Action |
|-------|------------|
| venv inside | Delete and create external venv in `../_venvs/` |
| __pycache__ | Delete all cache directories |
| logs/ folder | Archive to `../_artifacts/project/logs/` |
| .log files | Delete scattered log files |
| node_modules | Add to .cursorignore |
| Large files | Move to `../_data/project/` |
| Missing _AI_INCLUDE | Create with conventions and rules |
| Missing .cursorignore | Create with best practices |
| Missing bootstrap | Create bootstrap.sh and bootstrap.ps1 |

### 4. Backup System

Before fixing critical issues, Doctor creates a backup:

```
📦 Creating backup: project_backup_20251223_191137.tar.gz
✓ Backup created (15.2 MB)
```

Backups exclude: venv, node_modules, __pycache__, .git

## Interactive Mode

```
╔══════════════════════════════════════════════════════════════════╗
║  🏥 AI TOOLKIT DOCTOR — Project Analysis                         ║
╠══════════════════════════════════════════════════════════════════╣
║  Project: my_bot                                                  ║
║  Path:    /home/user/projects/my_bot                              ║
║  Tokens:  130K tokens (HIGH)                                      ║
╠══════════════════════════════════════════════════════════════════╣
║  🔴 CRITICAL ISSUES (1)                                          ║
║  ├─ [1] venv/ inside project                                      ║
║  🟡 WARNINGS (2)                                                 ║
║  ├─ [2] __pycache__/ in 5 locations                               ║
║  ├─ [3] logs/ folder (10 files)                                   ║
╠══════════════════════════════════════════════════════════════════╣
║  ACTIONS:                                                        ║
║  [1-9] Fix specific issue    [A] Fix ALL    [R] Report    [Q] Quit║
║  [T] Show full token breakdown                                   ║
╚══════════════════════════════════════════════════════════════════╝

> Enter choice: 
```

### Available Actions

- **[1-9]** — Fix specific issue by number
- **[A]** — Fix all issues automatically
- **[T]** — Show detailed token breakdown
- **[R]** — Regenerate PROJECT_STATUS.md
- **[Q]** — Quit without fixing

## CLI Options

### Basic Usage

```bash
python main.py doctor [PATH] [OPTIONS]
```

### Options

| Option | Description |
|--------|-------------|
| `PATH` | Project path (default: current directory) |
| `--auto`, `-a` | Auto-fix all issues without asking |
| `--report`, `-r` | Report only, don't offer fixes |

### Examples

```bash
# Diagnose current directory
python main.py doctor .

# Diagnose specific project
python main.py doctor /home/user/my_bot

# Auto-fix everything (CI/CD mode)
python main.py doctor /home/user/my_bot --auto

# Just show report (read-only)
python main.py doctor /home/user/my_bot --report
```

## Integration with Other Commands

### After Doctor runs:

1. **PROJECT_STATUS.md** is automatically updated
2. **CURRENT_CONTEXT_MAP.md** should be regenerated:
   ```bash
   python generate_map.py
   ```

### Recommended Workflow

```bash
# 1. Run doctor
python main.py doctor . --auto

# 2. Update context map
python generate_map.py

# 3. Verify with health check
python main.py health .

# 4. Commit changes
git add .
git commit -m "chore: optimize project with doctor"
```

## Token Thresholds

| Range | Status | Action |
|-------|--------|--------|
| < 100K | 🟢 OK | No action needed |
| 100K - 1M | 🟡 HIGH | Consider optimization |
| > 1M | 🔴 CRITICAL | Immediate optimization required |

## Best Practices

### 1. Run Doctor Regularly

```bash
# Weekly maintenance
python main.py doctor . --auto
```

### 2. Before Sharing Project

```bash
# Clean up before git push
python main.py doctor . --auto
git add .
git commit -m "chore: cleanup with doctor"
```

### 3. After Major Changes

```bash
# After adding new features
python main.py doctor .
# Review issues, fix manually or auto
```

### 4. CI/CD Integration

```yaml
# .github/workflows/doctor.yml
name: Doctor Check
on: [push, pull_request]
jobs:
  doctor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Doctor
        run: |
          python main.py doctor . --report
          # Fail if critical issues found
```

## Troubleshooting

### Doctor says "No issues found" but project is slow

Check:
1. Are large files in .cursorignore?
2. Run `python main.py doctor . --report` and press [T] for token breakdown
3. Look for files >5000 tokens and consider splitting them

### Backup failed

Check:
- Disk space available
- Write permissions in parent directory
- No files with special characters in names

### Fix failed

- Some fixes require manual intervention
- Check error message for details
- Try fixing manually then re-run doctor

## See Also

- [Token Calculation Guide](TOKEN_CALCULATION.md)
- [Project Optimization](OPTIMIZATION.md)
- [.cursorignore Best Practices](CURSORIGNORE.md)
