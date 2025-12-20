Если делать проект “с нуля” так, чтобы через 100 итераций не получить снова `venv/`, логи на сотни мегабайт и индексируемые зависимости, нужно сразу заложить 3 вещи:

1) **жёсткую структуру проекта** (где код, где данные, где логи)  
2) **файлы исключений** для Cursor/VS Code/Git  
3) **охранные правила** (скрипт/чек), который не позволит случайно создать `venv` внутри репо

Ниже — готовый “нулевой шаблон”: файлы + промпт для агента.

---

## 1) Рекомендуемая структура нового проекта

```
my_project/
  handlers/
  utils/
  api/
  webapp/                 # mini app
  parser/                 # или parser_faberlic_links/ если так привычнее
  database/
  scripts/
  _AI_INCLUDE/
  .vscode/
  .cursorignore
  .gitignore
  requirements.txt        # или pyproject.toml
  .env.example
  README.md
```

Снаружи репозитория (рядом с папкой проекта) будут жить тяжёлые вещи:

```
../_venvs/my_project-main
../_data/my_project/
../_artifacts/my_project/logs/
../_pw-browsers/          # если используешь Playwright
```

---

## 2) Файлы, которые создаёшь сразу

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

# Heavy artifacts/data (обычно не нужны для правок логики)
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

## 3) Скрипты, которые предотвращают повтор проблем

### `scripts/bootstrap.sh` (создаёт/переиспользует venv снаружи)
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

> `venv` — стандартный модуль Python для виртуальных окружений. Документация: https://docs.python.org/3/library/venv.html

### `scripts/check_repo_clean.sh` (охранник: не даёт случайно завести venv/мусор в репо)
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

Запускай его иногда вручную или повесь на pre-commit/CI.

---

## 4) Чтобы агент “не плодил дубликаты” — один универсальный промпт для новых проектов

Скопируй в Cursor Agent (когда создаёшь проект с 0):

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

## 5) Если в будущем появится Playwright
Чтобы не было повторных скачиваний/дубликатов браузеров, задавай общий кэш, например:
- `PLAYWRIGHT_BROWSERS_PATH=../_pw-browsers`
и делай установку один раз. Документация: https://playwright.dev/python/docs/browsers

---