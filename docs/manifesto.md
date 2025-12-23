# AI Toolkit Manifesto

The goal is to make things "beautiful" so that:

1) Cursor **doesn't index** gigabytes of garbage and doesn't consume tokens.  
2) Environments/artifacts **don't live in the project**, but can be **reused without duplicates**.  
3) The agent has a "reminder" so it doesn't create new `venv` inside the repo.

Below is a complete kit: `.cursorignore`, `.gitignore`, `.vscode/settings.json`, reminder `_AI_INCLUDE/...`, and 2 scripts: **isolate** (move out) and **restore** (bring back if really needed). Plus bootstrap (create venv outside and reuse).

---

## 1) `.cursorignore` (in root)

```gitignore
# --- Virtual environments / deps ---
venv/
.venv/
venv_gate/
parser_faberlic_links/.venv_parser/
**/.venv*/
**/site-packages/

# --- Python junk ---
**/__pycache__/
**/*.pyc
**/*.pyo

# --- Logs ---
logs/
*.log

# --- Playwright huge driver binaries ---
**/playwright/driver/

# --- Data/artifacts not needed for code edits ---
**/*.csv
**/*.jsonl
**/*.db
**/*.sqlite
**/*.sqlite3
```

This is key: Cursor will stop pulling `site-packages` and Playwright driver into context.

---

## 2) `.gitignore` (add if missing)

```gitignore
# Envs
venv/
.venv/
venv_gate/
**/.venv*/
parser_faberlic_links/.venv_parser/
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

# Local data
*.csv
*.jsonl
*.db
*.sqlite
*.sqlite3

# Playwright driver
**/playwright/driver/
```

---

## 3) `.vscode/settings.json` (so VS Code/Cursor doesn't search there either)

```json
{
  "files.exclude": {
    "**/venv": true,
    "**/.venv": true,
    "**/venv_gate": true,
    "**/.venv_parser": true,
    "**/site-packages": true,
    "**/__pycache__": true,
    "**/logs": true,
    "**/playwright/driver": true
  },
  "search.exclude": {
    "**/venv": true,
    "**/.venv": true,
    "**/venv_gate": true,
    "**/.venv_parser": true,
    "**/site-packages": true,
    "**/__pycache__": true,
    "**/logs": true,
    "**/playwright/driver": true,
    "**/*.pyc": true,
    "**/*.sqlite": true,
    "**/*.sqlite3": true,
    "**/*.db": true,
    "**/*.csv": true,
    "**/*.jsonl": true
  }
}
```

---

## 4) Agent Reminder (to avoid duplicates)

Create file: `_AI_INCLUDE/PROJECT_CONVENTIONS.md` (and DON'T ignore `_AI_INCLUDE`)

```md
# Project conventions (humans + AI)

## Source code (safe to read/edit)
handlers/
utils/
api/
webapp/
database/ (only *.py)
parser_faberlic_links/ (only source code)

## Never create environments inside the repo
Do NOT create: venv/, .venv/, venv_gate/, parser_faberlic_links/.venv_parser/
All venvs live outside the project:
../_venvs/<project>-main
../_venvs/<project>-gate
../_venvs/<project>-parser

Create/reuse venv only via:
scripts/bootstrap.sh  (Linux/macOS)
scripts/bootstrap.ps1 (Windows)

## Artifacts and data
Logs and dumps must NOT live in source folders.
Prefer external storage:
../_artifacts/<project>/logs
../_data/<project>/

## AI rules
- Never read/index site-packages, __pycache__, logs, playwright/driver
- Before creating a new env, check ../_venvs/ and reuse existing
- If you need an ignored file, ask user for a snippet or temporarily unignore exactly one file
```

---

## 5) Script "move all heavy stuff" (Linux/macOS)

`scripts/isolate_heavy.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJ="$(basename "$PWD")"

VENV_HOME="../_venvs"
ART_HOME="../_artifacts/${PROJ}"
DATA_HOME="../_data/${PROJ}"

mkdir -p "$VENV_HOME" "$ART_HOME" "$DATA_HOME"

move_if_exists () {
  local src="$1"
  local dst="$2"
  if [ -e "$src" ]; then
    echo "Move: $src -> $dst"
    rm -rf "$dst"
    mv "$src" "$dst"
  fi
}

# Environments -> ../_venvs (reuse without duplicates)
move_if_exists "venv"        "${VENV_HOME}/${PROJ}-main"
move_if_exists "venv_gate"   "${VENV_HOME}/${PROJ}-gate"
move_if_exists ".venv"       "${VENV_HOME}/${PROJ}-dotvenv"
move_if_exists "parser_faberlic_links/.venv_parser" "${VENV_HOME}/${PROJ}-parser"

# Logs -> ../_artifacts/<proj>/logs
if [ -d "logs" ]; then
  echo "Move: logs -> ${ART_HOME}/logs"
  mkdir -p "${ART_HOME}"
  rm -rf "${ART_HOME}/logs"
  mv "logs" "${ART_HOME}/logs"
fi

# Parser CSV dumps -> ../_data/<proj>/parser_csv (optional but nice)
if compgen -G "parser_faberlic_links/*.csv" > /dev/null; then
  mkdir -p "${DATA_HOME}/parser_csv"
  echo "Move: parser_faberlic_links/*.csv -> ${DATA_HOME}/parser_csv/"
  mv parser_faberlic_links/*.csv "${DATA_HOME}/parser_csv/" || true
fi

echo
echo "Done."
echo "Venvs:     ${VENV_HOME}/"
echo "Artifacts: ${ART_HOME}/"
echo "Data:      ${DATA_HOME}/"
```

Purpose: environments/logs/dumps go outside, **and no longer bloat the project**.

---

## 6) Script "restore back" (Linux/macOS)

This is an improved version of Claude's idea, but more careful (doesn't delete without need).

`scripts/restore_heavy.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJ="$(basename "$PWD")"

VENV_HOME="../_venvs"
ART_HOME="../_artifacts/${PROJ}"
DATA_HOME="../_data/${PROJ}"

restore_if_exists () {
  local src="$1"
  local dst="$2"
  if [ -e "$src" ]; then
    echo "Restore: $src -> $dst"
    rm -rf "$dst"
    mkdir -p "$(dirname "$dst")"
    mv "$src" "$dst"
  fi
}

# Restore envs back into repo (usually NOT needed; only if you really want to)
restore_if_exists "${VENV_HOME}/${PROJ}-main" "venv"
restore_if_exists "${VENV_HOME}/${PROJ}-gate" "venv_gate"
restore_if_exists "${VENV_HOME}/${PROJ}-dotvenv" ".venv"
restore_if_exists "${VENV_HOME}/${PROJ}-parser" "parser_faberlic_links/.venv_parser"

# Restore logs
if [ -d "${ART_HOME}/logs" ]; then
  echo "Restore: ${ART_HOME}/logs -> ./logs"
  rm -rf "logs"
  mv "${ART_HOME}/logs" "logs"
fi

# Restore CSV dumps
if [ -d "${DATA_HOME}/parser_csv" ]; then
  echo "Restore: ${DATA_HOME}/parser_csv/*.csv -> parser_faberlic_links/"
  mv "${DATA_HOME}/parser_csv/"*.csv "parser_faberlic_links/" 2>/dev/null || true
fi

echo "Done."
```

---

## 7) Bootstrap: to reuse environments, not multiply them

### Linux/macOS: `scripts/bootstrap.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJ="$(basename "$PWD")"
VENV_DIR="../_venvs/${PROJ}-main"

if [ ! -d "$VENV_DIR" ]; then
  echo "Create venv: $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python -m pip install -U pip wheel

if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  echo "No requirements.txt found. Create it (pip freeze > requirements.txt) in the currently working env."
fi

echo "Activate anytime: source $VENV_DIR/bin/activate"
```

### Windows: `scripts/bootstrap.ps1`

```powershell
$PROJ = Split-Path -Leaf (Get-Location)
$VENV_DIR = "..\_venvs\$PROJ-main"

if (-not (Test-Path $VENV_DIR)) {
  Write-Host "Create venv: $VENV_DIR"
  python -m venv $VENV_DIR
}

& "$VENV_DIR\Scripts\python.exe" -m pip install -U pip wheel

if (Test-Path .\requirements.txt) {
  & "$VENV_DIR\Scripts\pip.exe" install -r requirements.txt
} else {
  Write-Host "No requirements.txt found. Create it (pip freeze > requirements.txt) in the currently working env."
}

Write-Host "Activate: $VENV_DIR\Scripts\Activate.ps1"
```

---

## Answers to concerns "will we break the project?"

- **Removing/moving venv doesn't break the code**, only breaks the ability to run "right now" without recreating/activating the environment. Solved by bootstrap script and `requirements.txt`.
- **`.cursorignore`/exclude doesn't affect project operation at all**. It's only about indexing/context.
- "Will garbage keep appearing?" Yes: caches/logs/dumps will always appear. The difference is that now:
  - they live in known places,
  - are ignored,
  - Cursor doesn't index them.

---

## How to prevent agent from creating new duplicates
Your "contract" already solves this:

1) `_AI_INCLUDE/PROJECT_CONVENTIONS.md` — source of truth.  
2) Hard rule: "venv only in `../_venvs/` and only via `scripts/bootstrap.*`".  
3) If agent "needs data/logs" — it shouldn't pull the entire file, but request a **piece** or temporarily remove ignore from **one** file.

---

## Extended Documentation

Below are two ready artifacts:

1) `_AI_INCLUDE/WHERE_THINGS_LIVE.md` content (put in repo)  
2) Ready "Project Rules / System prompt" text for Cursor (paste in project/agent rules settings)

---

## 1) `_AI_INCLUDE/WHERE_THINGS_LIVE.md`

```md
# WHERE THINGS LIVE (single source of truth)

This file explains where in the project should be: source code, environments, logs, data and heavy artifacts.
Goal: don't multiply venv/dependencies duplicates and don't feed Cursor garbage that wastes tokens.

---

## 0) Definitions

- "Repo / project root" — repository root (where handlers/, webapp/, parser_faberlic_links/ etc. are located).
- "External dirs" — neighboring folders one level above repository.

Recommended external structure (next to repository):
../_venvs/
../_data/
../_artifacts/
../_pw-browsers/         (optional, shared Playwright browser cache)

---

## 1) Where source code lives (allowed to read/edit)

Allowed to analyze and modify:
- handlers/**
- utils/**
- api/**
- webapp/** (including webapp/v2/**)
- database/** (only source files *.py; DON'T touch large binary DB files unless necessary)
- parser_faberlic_links/** (only parser source code)

Forbidden to edit dependencies (site-packages) and generated artifacts.

---

## 2) Where virtual environments (venv) live

DO NOT create or store venv INSIDE the repository.

All venvs live outside, in:
../_venvs/<PROJECT>-main      # bot + backend + common dependencies
../_venvs/<PROJECT>-gate      # if you really need a separate "gate" (otherwise remove)
../_venvs/<PROJECT>-parser    # if parser needs separate dependencies

Rule: before creating a new environment, always check if the needed folder exists in ../_venvs/.
If it exists — reuse it, don't clone or create duplicates.

---

## 3) Where parser data and exports live

Data/exports SHOULD NOT be next to source code (so Cursor/search/indexing don't suffer).

Recommended locations:
- ../_data/<PROJECT>/parser_csv/          # *.csv (categories, all_products.csv etc.)
- ../_data/<PROJECT>/parser_dump/         # json/jsonl/html and other dumps (if any)

If you need small test data for unit tests — keep minimal example in repo:
- parser_faberlic_links/fixtures/**       # small files (KB, not MB)

---

## 4) Where logs live

Don't store logs in repository (or keep empty folder + .gitkeep).
Recommend:
- ../_artifacts/<PROJECT>/logs/

If log is needed for debugging — open/attach only relevant fragment, not the entire file.

---

## 5) Playwright

Heavy components:
- driver binaries inside site-packages (playwright/driver/*)
- downloaded browsers (chromium/firefox/webkit)

Rules:
- No edits/reading driver binaries.
- To avoid downloading browsers multiple times, use shared cache:
  environment variable PLAYWRIGHT_BROWSERS_PATH=../_pw-browsers
  and run browser installation once in this location.

---

## 6) What Cursor should ignore

Cursor should ignore entirely:
- venv/, .venv/, venv_gate/, parser_faberlic_links/.venv_parser/
- **/site-packages/
- **/__pycache__/, *.pyc
- logs/, *.log
- **/playwright/driver/
- large data: *.csv, *.sqlite*, *.db, *.jsonl (if these are artifacts, not sources)

---

## 7) If you suddenly need an ignored file

Algorithm:
1) Don't remove ignore from entire directory.
2) Ask user to explicitly specify 1 specific file or paste small fragment (200-500 lines).
3) If you can't do without the file — temporarily remove ignore pointwise for one path, then restore ignore back.

---

## 8) Anti-duplicates (important)

Never create inside repo:
- venv/
- venv_gate/
- .venv/
- parser_faberlic_links/.venv_parser/

Any pip/poetry/pdm commands are executed only in activated environment from ../_venvs/.
```

---

## 2) "Project Rules / System prompt" for Cursor

Paste this in project/agent rules in Cursor (where you set agent instructions). This is the "strictest" version so it doesn't eat tokens and doesn't multiply environments.

```text
You are an agent working on a Telegram bot + Mini App + parser repo.

PRIMARY GOAL
- Make functional changes only in project source code (bot, mini app, parser) with minimal context usage.

SOURCE CODE SCOPE (allowed to read/edit)
- handlers/**
- utils/**
- api/**
- webapp/** (including webapp/v2/**)
- database/** (only *.py code files; do NOT inspect big DB binaries unless user asks)
- parser_faberlic_links/** (only parser source code)

HARD EXCLUSIONS (never read, never index, never use as context)
- Any virtual env folders: venv/, .venv/, venv_gate/, parser_faberlic_links/.venv_parser/
- Any dependencies: **/site-packages/**
- Caches: **/__pycache__/**, **/*.pyc, **/*.pyo
- Logs: logs/**, *.log
- Playwright driver binaries: **/playwright/driver/**
- Large artifacts/data unless user explicitly requests: **/*.csv, **/*.sqlite, **/*.sqlite3, **/*.db, **/*.jsonl

ENVIRONMENT RULES (anti-duplication)
- NEVER create a venv inside the repo.
- Before creating any environment, check and reuse external envs:
  ../_venvs/<project>-main
  ../_venvs/<project>-gate
  ../_venvs/<project>-parser
- If an external env exists, reuse it; do not create duplicates.

ARTIFACT RULES
- Do not generate logs/dumps inside source directories.
- Prefer external locations:
  ../_artifacts/<project>/logs
  ../_data/<project>/
- If you need a log/data file, ask the user for a small snippet or request a single specific file. Never ingest entire large logs/datasets.

WORKFLOW RULES
- Do not "scan the whole codebase" by default.
- Ask for only the minimal set of files relevant to the requested change.
- When proposing changes, output exact diffs/patches and file paths.

REFERENCE
- Use _AI_INCLUDE/WHERE_THINGS_LIVE.md as the single source of truth for where things must live.
```

---

### Tip for this to actually work in Cursor
- Make sure `_AI_INCLUDE/` **is not ignored** and is visible to the agent.
- `.cursorignore` should already cut `venv/**` + `**/site-packages/**` + `**/playwright/driver/**` — this is the main consumer.
