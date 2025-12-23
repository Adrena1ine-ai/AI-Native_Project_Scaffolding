# 🛡️ PROJECT CONSTITUTION

> This file establishes the fundamental laws for AI agents working on this project.

---

## 1. STRATEGY

**`TECHNICAL_SPECIFICATION.md`** is the Roadmap.

- Defines phases and milestones
- Lists all features and their status
- Provides architectural overview

**Action:** Read this file to understand what the project is building.

---

## 2. TACTICS

**`_AI_INCLUDE/WHERE_THINGS_LIVE.md`** is the Law.

Derived from `first manifesto.md` — the foundational rules.

### Hard Rules:

1. **NO venv inside repo**
   - All virtual environments live in `../_venvs/`
   - Create via `scripts/bootstrap.sh`
   - Reuse existing envs, don't duplicate

2. **NO reading site-packages**
   - Never index or analyze dependencies
   - Never use site-packages content as context

3. **NO reading heavy artifacts**
   - Logs, CSVs, databases are off-limits
   - Ask for small snippets if needed

4. **Source code only**
   - Read/edit: `src/**`, `handlers/**`, `utils/**`, `api/**`
   - Ignore: `venv/`, `logs/`, `data/`, `*.csv`, `*.sqlite`

---

## 3. STATUS

**`PROJECT_STATUS.md`** tracks completion.

- What's implemented ✅
- What's next 🔜
- Test coverage stats

**Action:** Check this before assuming feature availability.

---

## 4. QUICK COMMANDS

| Action | Command |
|--------|---------|
| Run CLI | `python main.py` |
| Run wizard | `python main.py wizard` |
| Run tests | `pytest tests/ -v` |
| Update map | `python3 generate_map.py` |
| Benchmark | `python3 benchmark.py` |
| Bootstrap venv | `./scripts/bootstrap.sh` |
| Isolate artifacts | `./scripts/isolate_heavy.sh` |

---

## 5. AUTOMATION

**After creating or deleting files:**

```bash
python3 generate_map.py
```

Then read `CURRENT_CONTEXT_MAP.md` to update mental model.

---

## 6. PROHIBITIONS

### Never Create:
- `venv/`, `.venv/` inside project
- Duplicate files that already exist
- Russian text (comments, strings, docstrings)

### Never Read Entirely:
- `templates/**` — Output templates
- `tests/**` — Reference explicitly when needed
- `*.tar`, `*.log`, `*.csv` — Heavy data files
- `**/site-packages/**` — Dependencies

---

*This Constitution is derived from the First Manifesto and must be followed by all AI agents.*
