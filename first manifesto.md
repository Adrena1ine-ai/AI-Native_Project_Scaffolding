Делаем “красиво” и так, чтобы:

1) Cursor **не индексировал** гигабайты мусора и не жрал токены.  
2) Окружения/артефакты **не жили в проекте**, но при этом их можно было **переиспользовать без дубликатов**.  
3) У агента была “памятка”, чтобы он не создавал новые `venv` внутри репы.

Ниже — готовый комплект: `.cursorignore`, `.gitignore`, `.vscode/settings.json`, памятка `_AI_INCLUDE/...`, и 2 скрипта: **isolate** (вынести) и **restore** (вернуть обратно, если прям надо). Плюс bootstrap (создать venv снаружи и переиспользовать).

---

## 1) `.cursorignore` (в корне)

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

Это ключевое: Cursor перестанет тащить `site-packages` и Playwright driver в контекст.

---

## 2) `.gitignore` (добавь, если нет)

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

## 3) `.vscode/settings.json` (чтобы VS Code/Cursor не искал там тоже)

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

## 4) Памятка для агента (чтобы не плодил дубликаты)

Создай файл: `_AI_INCLUDE/PROJECT_CONVENTIONS.md` (и НЕ игнорируй `_AI_INCLUDE`)

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

## 5) Скрипт “вынести всё тяжёлое” (Linux/macOS)

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

# Environments -> ../_venvs (реюз без дубликатов)
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

# Parser CSV dumps -> ../_data/<proj>/parser_csv (опционально, но красиво)
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

Смысл: окружения/логи/дампы уходят наружу, **и больше не раздувают проект**.

---

## 6) Скрипт “вернуть обратно” (Linux/macOS)

Это улучшенная версия идеи Claude, но аккуратнее (ничего не удаляет без нужды).

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

# Restore envs back into repo (обычно НЕ надо; только если ты так хочешь)
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

## 7) Bootstrap: чтобы окружение не плодилось, а переиспользовалось

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

## Ответы на твои опасения “не сломаем ли проект?”

- **Удаление/вынос venv не ломает код**, ломает только возможность запускать “вот прямо сейчас” без пересоздания/активации окружения. Решается bootstrap-скриптом и `requirements.txt`.
- **`.cursorignore`/exclude вообще не влияет на работу проекта**. Это только про индексацию/контекст.
- “Будет ли дальше появляться мусор?” Да: кэши/логи/дампы всегда будут. Разница в том, что теперь:
  - они живут в понятных местах,
  - игнорируются,
  - Cursor их не индексирует.

---

## Как сделать, чтобы агент не создавал новые дубликаты
Твой “контракт” уже решает это:

1) `_AI_INCLUDE/PROJECT_CONVENTIONS.md` — источник правды.  
2) Жёсткое правило: “venv только в `../_venvs/` и только через `scripts/bootstrap.*`”.  
3) Если агенту “нужны данные/логи” — он не должен тащить весь файл, а попросить **кусок** или временно снять игнор с **одного** файла.

---

Если хочешь добить до идеала под твой проект: я могу дать ещё один маленький файл `_AI_INCLUDE/WHERE_THINGS_LIVE.md` с конкретными путями именно под твои папки (`venv_gate`, `parser_faberlic_links`) и готовый текст “System prompt/Project rules” для Cursor, чтобы агент автоматически следовал этим правилам.

Ниже два готовых артефакта:

1) содержимое файла `_AI_INCLUDE/WHERE_THINGS_LIVE.md` (кладёшь в репо)  
2) готовый текст “Project Rules / System prompt” для Cursor (вставляешь в настройки правил проекта/агента)

---

## 1) `_AI_INCLUDE/WHERE_THINGS_LIVE.md`

```md
# WHERE THINGS LIVE (single source of truth)

Этот файл объясняет, где в проекте должны находиться: исходники, окружения, логи, данные и тяжёлые артефакты.
Цель: не плодить дубликаты venv/зависимостей и не скармливать Cursor мусор, который тратит токены.

---

## 0) Определения

- "Repo / project root" — корень репозитория (где лежат handlers/, webapp/, parser_faberlic_links/ и т.д.).
- "External dirs" — соседние папки на уровень выше репозитория.

Рекомендуемая внешняя структура (рядом с репозиторием):
../_venvs/
../_data/
../_artifacts/
../_pw-browsers/         (опционально, общий кэш браузеров Playwright)

---

## 1) Где живёт исходный код (разрешено читать/править)

Разрешено анализировать и менять:
- handlers/**
- utils/**
- api/**
- webapp/** (включая webapp/v2/**)
- database/** (только исходники *.py; НЕ трогать большие бинарные файлы БД без необходимости)
- parser_faberlic_links/** (только исходники парсера)

Запрещено редактировать зависимости (site-packages) и генерируемые артефакты.

---

## 2) Где живут виртуальные окружения (venv)

ВНУТРИ репозитория venv НЕ создаём и НЕ храним.

Все venv живут снаружи, в:
../_venvs/<PROJECT>-main      # бот + backend + общие зависимости
../_venvs/<PROJECT>-gate      # если реально нужен отдельный "gate" (иначе убрать)
../_venvs/<PROJECT>-parser    # если парсер должен иметь отдельные зависимости

Правило: перед созданием нового окружения всегда проверять, существует ли нужная папка в ../_venvs/.
Если существует — переиспользовать, не клонировать и не создавать дубль.

---

## 3) Где живут данные парсера и выгрузки

Данные/выгрузки НЕ должны лежать рядом с исходниками (чтобы Cursor/поиск/индексация не страдали).

Рекомендуемые места:
- ../_data/<PROJECT>/parser_csv/          # *.csv (категории, all_products.csv и т.п.)
- ../_data/<PROJECT>/parser_dump/         # json/jsonl/html и прочие дампы (если есть)

Если нужны маленькие тестовые данные для unit-тестов — держать минимальный пример в repo:
- parser_faberlic_links/fixtures/**       # маленькие файлы (KB, не MB)

---

## 4) Где живут логи

Логи не храним в репозитории (или держим пустую папку + .gitkeep).
Рекомендуем:
- ../_artifacts/<PROJECT>/logs/

Если лог нужен для отладки — открывать/прикладывать только релевантный фрагмент, а не весь файл.

---

## 5) Playwright

Тяжёлые компоненты:
- driver binaries внутри site-packages (playwright/driver/*)
- скачанные браузеры (chromium/firefox/webkit)

Правила:
- Никаких правок/чтения driver бинарников.
- Чтобы не скачивать браузеры многократно, использовать общий кэш:
  переменная окружения PLAYWRIGHT_BROWSERS_PATH=../_pw-browsers
  и один раз выполнить установку браузеров в этом месте.

---

## 6) Что Cursor должен игнорировать

Cursor должен игнорировать целиком:
- venv/, .venv/, venv_gate/, parser_faberlic_links/.venv_parser/
- **/site-packages/
- **/__pycache__/, *.pyc
- logs/, *.log
- **/playwright/driver/
- большие данные: *.csv, *.sqlite*, *.db, *.jsonl (если это именно артефакты, не исходники)

---

## 7) Если внезапно нужен игнорируемый файл

Алгоритм:
1) Не снимать игнор со всего каталога.
2) Попросить пользователя явно указать 1 конкретный файл или вставить небольшой фрагмент (200–500 строк).
3) Если без файла нельзя — временно снять игнор точечно для одного пути, затем вернуть игнор обратно.

---

## 8) Анти-дубликаты (важно)

Никогда не создавать внутри repo:
- venv/
- venv_gate/
- .venv/
- parser_faberlic_links/.venv_parser/

Любые команды pip/poetry/pdm выполняются только в активированном окружении из ../_venvs/.
```

---

## 2) “Project Rules / System prompt” для Cursor

Вставь это в правила проекта/агента в Cursor (там, где у тебя задаются инструкции для агента). Это максимально “жёсткий” вариант, чтобы он не жрал токены и не плодил окружения.

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
- Do not “scan the whole codebase” by default.
- Ask for only the minimal set of files relevant to the requested change.
- When proposing changes, output exact diffs/patches and file paths.

REFERENCE
- Use _AI_INCLUDE/WHERE_THINGS_LIVE.md as the single source of truth for where things must live.
```

---

### Мини-совет, чтобы это реально работало в Cursor
- Убедись, что `_AI_INCLUDE/` **не игнорируется** и виден агенту.
- `.cursorignore` уже должен резать `venv/**` + `**/site-packages/**` + `**/playwright/driver/**` — это главный пожиратель.
