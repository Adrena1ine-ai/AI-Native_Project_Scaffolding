# WHERE THINGS LIVE (single source of truth)

This file explains where in the project things should live: source code, environments, logs, data, and heavy artifacts.
Goal: avoid duplicating venvs/dependencies and prevent Cursor from consuming garbage that wastes tokens.

---

## 0) Definitions

- "Repo / project root" — repository root (where handlers/, webapp/, src/ etc. live).
- "External dirs" — neighboring folders one level above the repository.

Recommended external structure (next to repository):
```
../_venvs/
../_data/
../_artifacts/
../_pw-browsers/         (optional, shared Playwright browser cache)
```

---

## 1) Where source code lives (allowed to read/edit)

Allowed to analyze and modify:
- src/**
- handlers/**
- utils/**
- api/**
- webapp/**
- database/** (only source *.py files; do NOT touch large DB binaries unnecessarily)
- parser_*/** (only parser source code)

Forbidden to edit dependencies (site-packages) and generated artifacts.

---

## 2) Where virtual environments (venv) live

DO NOT create or store venv INSIDE the repository.

All venvs live outside, in:
```
../_venvs/<PROJECT>-main      # bot + backend + common dependencies
../_venvs/<PROJECT>-gate      # if separate "gate" env is truly needed
../_venvs/<PROJECT>-parser    # if parser needs separate dependencies
```

Rule: before creating a new environment, always check if the needed folder exists in `../_venvs/`.
If it exists — reuse it, do not clone or create duplicates.

---

## 3) Where parser data and exports live

Data/exports should NOT live next to source code (so Cursor/search/indexing don't suffer).

Recommended locations:
- `../_data/<PROJECT>/parser_csv/`          # *.csv (categories, all_products.csv etc.)
- `../_data/<PROJECT>/parser_dump/`         # json/jsonl/html and other dumps

If small test data is needed for unit tests — keep minimal example in repo:
- `tests/fixtures/**`       # small files (KB, not MB)

---

## 4) Where logs live

Do not store logs in repository (or keep an empty folder + .gitkeep).
Recommended:
- `../_artifacts/<PROJECT>/logs/`

If a log is needed for debugging — open/attach only the relevant fragment, not the entire file.

---

## 5) Playwright

Heavy components:
- driver binaries inside site-packages (playwright/driver/*)
- downloaded browsers (chromium/firefox/webkit)

Rules:
- No editing/reading of driver binaries.
- To avoid downloading browsers multiple times, use shared cache:
  environment variable `PLAYWRIGHT_BROWSERS_PATH=../_pw-browsers`
  and install browsers once in that location.

---

## 6) What Cursor must ignore

Cursor must ignore entirely:
- venv/, .venv/, venv_gate/, parser_*/.venv_parser/
- **/site-packages/
- **/__pycache__/, *.pyc
- logs/, *.log
- **/playwright/driver/
- large data: *.csv, *.sqlite*, *.db, *.jsonl (if artifacts, not source)
- _AI_ARCHIVE/

---

## 7) If an ignored file is suddenly needed

Algorithm:
1) Do not remove ignore from entire directory.
2) Ask user to explicitly specify 1 specific file or paste a small fragment (200-500 lines).
3) If file is essential — temporarily remove ignore for one path only, then restore ignore.

---

## 8) Anti-duplicates (important)

Never create inside repo:
- venv/
- venv_gate/
- .venv/
- parser_*/.venv_parser/

Any pip/poetry/pdm commands are executed only in activated environment from `../_venvs/`.

---

*Derived from the First Manifesto — the foundational rules for AI-native projects.*

