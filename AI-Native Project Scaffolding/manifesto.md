# AI-Native Project Scaffolding Manifesto

When starting a project from scratch, to avoid ending up with `venv/`, logs of hundreds of megabytes, and indexed dependencies after 100 iterations, you need to establish 3 things right away:

1) **A strict project structure** (where code, data, and logs live)
2) **Exclusion files** for Cursor/VS Code/Git
3) **Protective rules** (script/check) that prevent accidentally creating `venv` inside the repo

Below is a ready-to-use "zero template": files + prompt for the agent.

---

## 1) Recommended Structure for a New Project

```
my_project/
  handlers/
  utils/
  api/
  webapp/                 # mini app
  parser/
  database/
  scripts/
  _AI_INCLUDE/
  .vscode/
  .cursorignore
  .gitignore
  requirements.txt        # or pyproject.toml
  .env.example
  README.md
```

Outside the repository (next to the project folder) will live heavy things:

```
../_venvs/my_project-main
../_data/my_project/
../_artifacts/my_project/logs/
../_pw-browsers/          # if using Playwright
```

---

## 2) Files to Create Immediately

### `.cursorignore`
```gitignore
# Environments / deps
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

# Heavy artifacts/data (usually not needed for logic edits)
**/*.csv
**/*.jsonl
**/*.db
**/*.sqlite
**/*.sqlite3

# Playwright
**/playwright/driver/
```

### `.gitignore`
```gitignore
# Envs
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
```

### `.vscode/settings.json`
```json
{
  "search.exclude": {
    "**/venv": true,
    "**/.venv": true,
    "**/.venv*": true,
    "**/site-packages": true,
    "**/__pycache__": true,
    "**/logs": true,
    "**/node_modules": true,
    "**/dist": true,
    "**/build": true,
    "**/.next": true,
    "**/*.pyc": true,
    "**/*.csv": true,
    "**/*.sqlite": true,
    "**/*.sqlite3": true,
    "**/*.db": true,
    "**/*.jsonl": true,
    "**/playwright/driver": true
  },
  "files.exclude": {
    "**/venv": true,
    "**/.venv": true,
    "**/.venv*": true,
    "**/site-packages": true,
    "**/__pycache__": true,
    "**/node_modules": true
  }
}
```

### `_AI_INCLUDE/PROJECT_CONVENTIONS.md`
```md
# Project conventions (humans + AI)

## Source code to read/edit
handlers/, utils/, api/, webapp/, parser/, database/ (*.py only)

## Never create venv inside repo
Do NOT create: venv/, .venv/, */.venv*/
Use external venv only:
../_venvs/<project>-main

Create/reuse it via scripts/bootstrap.(sh|ps1)

## Artifacts
Logs: ../_artifacts/<project>/logs
Data dumps: ../_data/<project>/
Never commit or index large dumps/logs.
```

---

## 3) Scripts That Prevent Repeated Problems

### `scripts/bootstrap.sh` (creates/reuses venv outside)
```bash
#!/usr/bin/env bash
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
```

> `venv` is Python's standard module for virtual environments. Documentation: https://docs.python.org/3/library/venv.html

### `scripts/check_repo_clean.sh` (guard: prevents accidentally adding venv/junk to repo)
```bash
#!/usr/bin/env bash
set -euo pipefail

bad=0
for p in venv .venv; do
  if [ -d "$p" ]; then
    echo "ERROR: forbidden directory in repo: $p"
    bad=1
  fi
done

if find . -path "*/site-packages" -prune -print | grep -q .; then
  echo "ERROR: site-packages found inside repo"
  bad=1
fi

exit $bad
```

Run it occasionally by hand or hook it up to pre-commit/CI.

---

## 4) Universal Prompt for New Projects (to prevent duplicates)

Copy into Cursor Agent (when creating a project from scratch):

```text
Bootstrap a new repo for a Telegram bot + Mini App + Python parser with strict hygiene.

Do the following in the repository root:

1) Create these files with exact content:
- .cursorignore (exclude venv/.venv/site-packages/__pycache__/logs/node_modules/build artifacts/data dumps/playwright driver)
- .gitignore (same exclusions + .env)
- .vscode/settings.json (files.exclude + search.exclude for the same heavy paths)
- _AI_INCLUDE/PROJECT_CONVENTIONS.md (single source of truth: code vs env vs artifacts)
- scripts/bootstrap.sh and scripts/bootstrap.ps1 to create/reuse external venv at ../_venvs/<project>-main
- scripts/check_repo_clean.sh (fails if venv/.venv/site-packages exists inside repo)

2) Enforce rules:
- Never create venv inside repo.
- Never modify or read site-packages.
- Logs go to ../_artifacts/<project>/logs, data dumps to ../_data/<project>/.
- If any ignored file is needed, ask for a small snippet or explicitly request a single file.

3) Create a minimal folder structure:
handlers/, utils/, api/, webapp/, parser/, database/, scripts/, _AI_INCLUDE/, .vscode/

Output: show the exact file contents or patches for everything you create/change.
```

---

## 5) If Playwright is Needed in the Future

To avoid repeated downloads/duplicate browsers, set a shared cache, e.g.:
- `PLAYWRIGHT_BROWSERS_PATH=../_pw-browsers`
and install once. Documentation: https://playwright.dev/python/docs/browsers

---
