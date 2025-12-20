# 🚀 Универсальный генератор проекта

#Один скрипт — полная структура за минуту!



#!/usr/bin/env python3
"""
🚀 Генератор проекта: Telegram Bot + Mini App + Scripts
Создаёт полную структуру с правильной конфигурацией для Cursor

Использование:
    python create_project.py my_awesome_bot
    python create_project.py my_bot --path /home/user/projects
"""

import argparse
import os
import stat
from pathlib import Path
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
# ШАБЛОНЫ ФАЙЛОВ
# ═══════════════════════════════════════════════════════════════

CURSORIGNORE = '''# ═══════════════════════════════════════
# CURSOR IGNORE — НЕ ИНДЕКСИРОВАТЬ
# Сгенерировано: {date}
# ═══════════════════════════════════════

# === ВИРТУАЛЬНЫЕ ОКРУЖЕНИЯ ===
venv/
.venv/
env/
.env/
**/venv/
**/.venv/
**/site-packages/
**/lib/python*/
**/Lib/site-packages/
**/Scripts/
**/bin/python*

# === PLAYWRIGHT ===
**/playwright/driver/
**/playwright/.local-browsers/
**/.cache/ms-playwright/

# === PYTHON КЭШИ ===
__pycache__/
**/__pycache__/
*.py[cod]
*$py.class
*.pyo
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# === ЛОГИ ===
logs/
*.log
*.log.*

# === ДАННЫЕ ===
data/
artifacts/
*.csv
*.sqlite3
*.sqlite
*.db

# === БИНАРНИКИ ===
*.exe
*.so
*.dll
*.dylib

# === АССЕТЫ ===
assets/
*.png
*.jpg
*.jpeg
*.gif
*.ico
*.webp
*.woff
*.woff2
*.ttf
*.eot

# === АРХИВЫ ===
*.zip
*.tar
*.tar.gz
*.rar
*.7z

# === GIT ===
.git/

# === NODE ===
node_modules/
package-lock.json
yarn.lock

# === СЕКРЕТЫ ===
.env
.env.*
!.env.example
*.pem
*.key
*.secret

# === IDE ===
.idea/
.vscode/settings.json
*.swp
*.swo
*~
'''

CURSORRULES = '''# ═══════════════════════════════════════════════════════════
# ПРАВИЛА ДЛЯ AI — {project_name}
# Сгенерировано: {date}
# ═══════════════════════════════════════════════════════════

## 🧠 ПЕРВОЕ ДЕЙСТВИЕ ПРИ ЛЮБОМ ЗАПРОСЕ

1. Прочитай `_AI_INCLUDE/` — там ВСЕ пути и правила
2. Проверь существующие файлы перед созданием
3. Следуй структуре проекта

---

## 🚫 АБСОЛЮТНЫЕ ЗАПРЕТЫ

### Никогда не создавай внутри проекта:
- `venv/`, `.venv/`, `env/` — окружения хранятся в `../_venvs/`
- Дубликаты существующих файлов
- Новые requirements.txt в подпапках

### Никогда не читай целиком:
- `logs/*.log` → используй `tail -50`
- `data/*.csv` → используй `head -10`
- `*.sqlite3` → используй SQL запросы
- Любые файлы > 100KB без явной необходимости

---

## ✅ ПРАВИЛЬНЫЕ ДЕЙСТВИЯ

### Новый Python-пакет:
```bash
source ../_venvs/{project_name}-venv/bin/activate
pip install <package>
pip freeze > requirements.txt
```

### Данные из CSV:
```bash
head -10 data/file.csv
grep -i "поиск" data/file.csv | head -5
wc -l data/file.csv
```

### Структура БД:
```bash
sqlite3 database/app.sqlite3 ".schema"
sqlite3 database/app.sqlite3 "SELECT * FROM table LIMIT 5"
```

### Логи:
```bash
tail -50 logs/bot.log
grep -i "error" logs/bot.log | tail -20
```

---

## 📍 СТРУКТУРА ПРОЕКТА

### Код (читай/редактируй свободно):
```
bot/                 — Telegram бот
├── handlers/        — обработчики команд
├── keyboards/       — клавиатуры
├── utils/           — утилиты
├── middlewares/     — middleware
└── main.py          — точка входа

webapp/              — Mini App (HTML/JS/CSS)
scripts/             — Python скрипты
database/db.py       — работа с БД
api/                 — веб-сервер
config.py            — конфигурация
_AI_INCLUDE/         — документация (ЧИТАЙ!)
```

### Данные (читай по запросу, не целиком):
```
data/                — CSV, JSON файлы
logs/                — логи
artifacts/           — временные файлы
database/*.sqlite3   — база данных
```

### Окружения (ВНЕ проекта):
```
../_venvs/{project_name}-venv/   — Python venv
../_pw-browsers/                  — Playwright Chromium
```

---

## 🔄 ЧЕКЛИСТ ПЕРЕД СОЗДАНИЕМ ФАЙЛА

1. ⏸️ СТОП
2. 📖 Проверь `_AI_INCLUDE/WHERE_THINGS_LIVE.md`
3. ❓ Такой файл уже существует?
4. 📁 Правильная ли папка?
5. ✅ Создавай

---

## 💬 ФОРМАТ ОТВЕТОВ

### Создание файла:
```
📁 Создаю: bot/handlers/new_feature.py
📍 Проверил: файла нет, папка существует
```

### Нужны данные:
```
📊 Мне нужны данные. Выполни:
   head -10 data/products.csv
```

### Нужен пакет:
```
📦 Нужен пакет: aiofiles
   source ../_venvs/{project_name}-venv/bin/activate
   pip install aiofiles
   pip freeze > requirements.txt
```
'''

PROJECT_CONVENTIONS = '''# 📜 КОНТРАКТ ПРОЕКТА — {project_name}

> Этот документ — закон. AI и люди следуют ему.

---

## 🎯 Назначение проекта

Telegram бот + Mini App + вспомогательные скрипты.

---

## 📁 Структура и ответственность

| Папка | Назначение | Редактировать |
|-------|------------|---------------|
| `bot/` | Telegram бот (aiogram) | ✅ Да |
| `bot/handlers/` | Обработчики команд | ✅ Да |
| `bot/keyboards/` | Клавиатуры | ✅ Да |
| `bot/utils/` | Утилиты бота | ✅ Да |
| `bot/middlewares/` | Middleware | ✅ Да |
| `webapp/` | Mini App (HTML/JS/CSS) | ✅ Да |
| `scripts/` | Вспомогательные скрипты | ✅ Да |
| `database/` | Работа с БД | ✅ Да |
| `api/` | API сервер | ✅ Да |
| `data/` | Данные (CSV, JSON) | ⚠️ Генерируется |
| `logs/` | Логи | ❌ Автоматически |
| `artifacts/` | Временные файлы | ⚠️ Очищается |
| `_AI_INCLUDE/` | Документация для AI | ✅ Да |

---

## 🐍 Виртуальные окружения

### ⚠️ КРИТИЧЕСКИ ВАЖНО

Окружения хранятся **ВНЕ проекта** в `../_venvs/`

```
../_venvs/
└── {project_name}-venv/    # Python {python_version}
```

### Почему так?
- Не раздувает проект (экономия 200-800 MB)
- Cursor не индексирует
- Легко пересоздать из requirements.txt
- Можно шарить между проектами

### Создание:
```bash
./scripts/bootstrap.sh
```

### Активация:
```bash
# Linux/Mac
source ../_venvs/{project_name}-venv/bin/activate

# Windows
..\_venvs\{project_name}-venv\Scripts\Activate.ps1
```

### Добавление пакета:
```bash
source ../_venvs/{project_name}-venv/bin/activate
pip install <package>
pip freeze > requirements.txt
```

---

## 🎭 Playwright (если используется)

Браузеры в общем кэше:
```
../_pw-browsers/
```

Переменная:
```bash
export PLAYWRIGHT_BROWSERS_PATH=../_pw-browsers
```

Установка:
```bash
playwright install chromium  # Только Chromium!
```

---

## 📦 Артефакты и данные

| Папка | Что там | Игнорируется | Очищать |
|-------|---------|--------------|---------|
| `data/` | CSV, JSON данные | ✅ Да | По необходимости |
| `logs/` | Логи приложения | ✅ Да | Ротация |
| `artifacts/` | Временные файлы | ✅ Да | Регулярно |
| `database/*.sqlite3` | SQLite БД | ✅ Да | Бэкапить |

---

## 🚫 Правила для AI

### Перед созданием ЛЮБОГО файла:
1. Проверь `WHERE_THINGS_LIVE.md`
2. Убедись что файла нет
3. Используй правильную папку

### Запрещено:
- Создавать venv внутри проекта
- Дублировать существующие файлы
- Читать большие файлы целиком
- Менять структуру без согласования

### Разрешено:
- Создавать файлы в правильных папках
- Предлагать новые пакеты через pip
- Читать фрагменты данных через head/tail/grep
'''

WHERE_THINGS_LIVE = '''# 🗺️ ГДЕ ЧТО ЛЕЖИТ — {project_name}

> Перед созданием файла — сверься здесь!

---

## 📂 Исходный код

```
{project_name}/
│
├── bot/                          # Telegram бот
│   ├── __init__.py
│   ├── main.py                   # 🚀 Точка входа бота
│   ├── handlers/                 # Обработчики
│   │   ├── __init__.py
│   │   ├── start.py              # /start, /help
│   │   ├── common.py             # Общие команды
│   │   └── ...                   # Другие handlers
│   ├── keyboards/                # Клавиатуры
│   │   ├── __init__.py
│   │   ├── inline.py             # Inline кнопки
│   │   └── reply.py              # Reply кнопки
│   ├── utils/                    # Утилиты
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── middlewares/              # Middleware
│       ├── __init__.py
│       └── logging.py
│
├── webapp/                       # Mini App
│   ├── index.html                # Главная страница
│   ├── app.js                    # JavaScript логика
│   ├── styles.css                # Стили
│   └── assets/                   # Статика (иконки и т.д.)
│
├── scripts/                      # Скрипты
│   ├── bootstrap.sh              # Создание окружения
│   ├── bootstrap.ps1             # Windows версия
│   └── ...                       # Другие скрипты
│
├── database/                     # База данных
│   ├── __init__.py
│   ├── db.py                     # Логика работы с БД
│   └── app.sqlite3               # [ИГНОР] Файл БД
│
├── api/                          # API сервер
│   ├── __init__.py
│   └── server.py                 # Веб-сервер
│
└── config.py                     # Конфигурация
```

---

## 📊 Данные (игнорируются Cursor)

```
data/                             # Данные приложения
├── *.csv                         # CSV файлы
├── *.json                        # JSON файлы
└── ...

logs/                             # Логи
└── bot.log                       # Основной лог

artifacts/                        # Временные файлы
└── ...
```

### Как читать данные:
```bash
# CSV — заголовки и первые строки
head -10 data/file.csv

# Поиск в CSV
grep -i "запрос" data/file.csv | head -10

# Количество строк
wc -l data/file.csv

# JSON — форматированный вывод
cat data/file.json | python -m json.tool | head -50
```

---

## 🗄️ База данных

**Путь:** `database/app.sqlite3`

### Как работать:
```bash
# Структура таблиц
sqlite3 database/app.sqlite3 ".schema"

# Список таблиц
sqlite3 database/app.sqlite3 ".tables"

# Примеры данных
sqlite3 database/app.sqlite3 "SELECT * FROM users LIMIT 5"
```

---

## 📝 Логи

**Путь:** `logs/bot.log`

### Как читать:
```bash
# Последние записи
tail -50 logs/bot.log

# Ошибки
grep -i "error\\|exception" logs/bot.log | tail -20

# В реальном времени
tail -f logs/bot.log
```

---

## 🔧 Конфигурация

```
.env.example          # Пример переменных (✅ читать)
.env                  # Секреты (❌ НЕ читать!)
config.py             # Python конфигурация
requirements.txt      # Зависимости
```

---

## 🐍 Виртуальное окружение

### ❌ НЕ здесь (внутри проекта):
```
./venv/               # НЕ СОЗДАВАТЬ!
./.venv/              # НЕ СОЗДАВАТЬ!
./env/                # НЕ СОЗДАВАТЬ!
```

### ✅ Здесь (вне проекта):
```
../_venvs/{project_name}-venv/
├── bin/              # Linux/Mac
│   ├── python
│   ├── pip
│   └── activate
└── Scripts/          # Windows
    ├── python.exe
    └── Activate.ps1
```

### Активация:
```bash
# Linux/Mac
source ../_venvs/{project_name}-venv/bin/activate

# Windows
..\_venvs\{project_name}-venv\Scripts\Activate.ps1
```

---

## 🎭 Playwright (если есть)

```
../_pw-browsers/
└── chromium-*/       # Только Chromium
```

Переменная: `PLAYWRIGHT_BROWSERS_PATH=../_pw-browsers`

---

## 📁 Служебные папки

```
_AI_INCLUDE/          # ✅ Документация — ЧИТАТЬ ВСЕГДА
.git/                 # ❌ Git — игнорировать
__pycache__/          # ❌ Кэш — игнорировать
```

---

## 🚨 Быстрая проверка

| Хочу | Проверь | Правильный путь |
|------|---------|-----------------|
| Новый handler | `bot/handlers/` | `bot/handlers/name.py` |
| Новая клавиатура | `bot/keyboards/` | `bot/keyboards/name.py` |
| Утилита бота | `bot/utils/` | `bot/utils/name.py` |
| Страница Mini App | `webapp/` | `webapp/page.html` |
| Скрипт | `scripts/` | `scripts/name.py` |
| Сохранить данные | `data/` | `data/name.csv` |
| Новый venv | `../_venvs/` | НЕ в проекте! |
'''

DEPENDENCIES = '''# 📦 ЗАВИСИМОСТИ — {project_name}

## Текущие пакеты

| Пакет | Версия | Назначение |
|-------|--------|------------|
| aiogram | 3.x | Telegram Bot API |
| aiohttp | 3.x | Async HTTP клиент/сервер |
| pydantic | 2.x | Валидация данных |
| pydantic-settings | 2.x | Настройки из .env |
| python-dotenv | 1.x | Загрузка .env |
| aiosqlite | 0.19+ | Async SQLite |

## Файл зависимостей

`requirements.txt` в корне проекта

## Установка с нуля

```bash
# 1. Запустить bootstrap
./scripts/bootstrap.sh

# 2. Или вручную
python -m venv ../_venvs/{project_name}-venv
source ../_venvs/{project_name}-venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Добавление пакета

```bash
# 1. Активировать окружение
source ../_venvs/{project_name}-venv/bin/activate

# 2. Установить
pip install <package>

# 3. Обновить requirements.txt
pip freeze > requirements.txt

# 4. Закоммитить requirements.txt
git add requirements.txt
git commit -m "Add <package>"
```

## Обновление пакетов

```bash
source ../_venvs/{project_name}-venv/bin/activate

# Обновить конкретный
pip install --upgrade <package>

# Обновить все
pip install --upgrade -r requirements.txt

# Сохранить
pip freeze > requirements.txt
```

## Playwright (если нужен)

```bash
# Установить пакет
pip install playwright

# Установить только Chromium
export PLAYWRIGHT_BROWSERS_PATH=../_pw-browsers
playwright install chromium

# Обновить requirements.txt
pip freeze > requirements.txt
```
'''

BOOTSTRAP_SH = '''#!/bin/bash
# ═══════════════════════════════════════════════════════════
# Bootstrap скрипт — {project_name}
# Создание и настройка окружения
# ═══════════════════════════════════════════════════════════

set -e

# Цвета
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

# Пути
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_NAME="$(basename "$PROJECT_DIR")"
VENVS_DIR="$(dirname "$PROJECT_DIR")/_venvs"
VENV_PATH="$VENVS_DIR/$PROJECT_NAME-venv"
PW_BROWSERS="$(dirname "$PROJECT_DIR")/_pw-browsers"

echo -e "${{BLUE}}═══════════════════════════════════════════════════════════${{NC}}"
echo -e "${{BLUE}}🚀 Bootstrap: $PROJECT_NAME${{NC}}"
echo -e "${{BLUE}}═══════════════════════════════════════════════════════════${{NC}}"
echo ""
echo -e "📁 Проект:    $PROJECT_DIR"
echo -e "🐍 Venv:      $VENV_PATH"
echo -e "🎭 Browsers:  $PW_BROWSERS"
echo ""

# ═══ Создание директорий ═══
echo -e "${{YELLOW}}📂 Создаю директории...${{NC}}"
mkdir -p "$VENVS_DIR"
mkdir -p "$PW_BROWSERS"
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/data"
mkdir -p "$PROJECT_DIR/artifacts"
echo -e "${{GREEN}}   ✓ Директории созданы${{NC}}"

# ═══ Виртуальное окружение ═══
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${{YELLOW}}🐍 Создаю виртуальное окружение...${{NC}}"
    python3 -m venv "$VENV_PATH"
    
    echo -e "${{YELLOW}}📦 Устанавливаю pip...${{NC}}"
    source "$VENV_PATH/bin/activate"
    pip install --upgrade pip --quiet
    
    if [ -f "$PROJECT_DIR/requirements.txt" ]; then
        echo -e "${{YELLOW}}📦 Устанавливаю зависимости...${{NC}}"
        pip install -r "$PROJECT_DIR/requirements.txt" --quiet
    fi
    
    deactivate
    echo -e "${{GREEN}}   ✓ Окружение создано${{NC}}"
else
    echo -e "${{GREEN}}   ✓ Окружение уже существует${{NC}}"
fi

# ═══ Проверка старых venv в проекте ═══
echo ""
echo -e "${{YELLOW}}🔍 Проверяю старые окружения в проекте...${{NC}}"
FOUND_OLD=false
for old_venv in "venv" ".venv" "env" ".env"; do
    if [ -d "$PROJECT_DIR/$old_venv" ] && [ "$old_venv" != ".env" ]; then
        echo -e "${{RED}}   ⚠️  Найден $old_venv/ внутри проекта!${{NC}}"
        FOUND_OLD=true
    fi
done

if [ "$FOUND_OLD" = true ]; then
    echo ""
    read -p "   Удалить старые окружения из проекта? (y/N): " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        for old_venv in "venv" ".venv" "env"; do
            if [ -d "$PROJECT_DIR/$old_venv" ]; then
                rm -rf "$PROJECT_DIR/$old_venv"
                echo -e "${{GREEN}}   ✓ Удалён $old_venv/${{NC}}"
            fi
        done
    fi
else
    echo -e "${{GREEN}}   ✓ Старых окружений не найдено${{NC}}"
fi

# ═══ .env файл ═══
echo ""
if [ ! -f "$PROJECT_DIR/.env" ] && [ -f "$PROJECT_DIR/.env.example" ]; then
    echo -e "${{YELLOW}}📝 Создаю .env из .env.example...${{NC}}"
    cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
    echo -e "${{GREEN}}   ✓ .env создан — отредактируй его!${{NC}}"
fi

# ═══ Итоги ═══
echo ""
echo -e "${{GREEN}}═══════════════════════════════════════════════════════════${{NC}}"
echo -e "${{GREEN}}✅ Bootstrap завершён!${{NC}}"
echo -e "${{GREEN}}═══════════════════════════════════════════════════════════${{NC}}"
echo ""
echo -e "Следующие шаги:"
echo ""
echo -e "  1. Активируй окружение:"
echo -e "     ${{BLUE}}source $VENV_PATH/bin/activate${{NC}}"
echo ""
echo -e "  2. Настрой .env:"
echo -e "     ${{BLUE}}nano .env${{NC}}"
echo ""
echo -e "  3. Запусти бота:"
echo -e "     ${{BLUE}}python bot/main.py${{NC}}"
echo ""
'''

BOOTSTRAP_PS1 = '''# ═══════════════════════════════════════════════════════════
# Bootstrap скрипт — {project_name}
# Windows PowerShell
# ═══════════════════════════════════════════════════════════

$ErrorActionPreference = "Stop"

# Пути
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir
$ProjectName = Split-Path -Leaf $ProjectDir
$VenvsDir = Join-Path (Split-Path -Parent $ProjectDir) "_venvs"
$VenvPath = Join-Path $VenvsDir "$ProjectName-venv"
$PwBrowsers = Join-Path (Split-Path -Parent $ProjectDir) "_pw-browsers"

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Blue
Write-Host "🚀 Bootstrap: $ProjectName" -ForegroundColor Blue
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Blue
Write-Host ""
Write-Host "📁 Проект:    $ProjectDir"
Write-Host "🐍 Venv:      $VenvPath"
Write-Host "🎭 Browsers:  $PwBrowsers"
Write-Host ""

# Создание директорий
Write-Host "📂 Создаю директории..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $VenvsDir | Out-Null
New-Item -ItemType Directory -Force -Path $PwBrowsers | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectDir\\logs" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectDir\\data" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectDir\\artifacts" | Out-Null
Write-Host "   ✓ Директории созданы" -ForegroundColor Green

# Виртуальное окружение
if (-not (Test-Path $VenvPath)) {{
    Write-Host "🐍 Создаю виртуальное окружение..." -ForegroundColor Yellow
    python -m venv $VenvPath
    
    Write-Host "📦 Устанавливаю зависимости..." -ForegroundColor Yellow
    & "$VenvPath\\Scripts\\Activate.ps1"
    pip install --upgrade pip --quiet
    
    $ReqFile = Join-Path $ProjectDir "requirements.txt"
    if (Test-Path $ReqFile) {{
        pip install -r $ReqFile --quiet
    }}
    
    deactivate
    Write-Host "   ✓ Окружение создано" -ForegroundColor Green
}} else {{
    Write-Host "   ✓ Окружение уже существует" -ForegroundColor Green
}}

# Проверка старых venv
Write-Host ""
Write-Host "🔍 Проверяю старые окружения..." -ForegroundColor Yellow
$OldVenvs = @("venv", ".venv", "env")
$FoundOld = $false

foreach ($old in $OldVenvs) {{
    $OldPath = Join-Path $ProjectDir $old
    if (Test-Path $OldPath) {{
        Write-Host "   ⚠️  Найден $old/ внутри проекта!" -ForegroundColor Red
        $FoundOld = $true
    }}
}}

if ($FoundOld) {{
    $confirm = Read-Host "   Удалить старые окружения? (y/N)"
    if ($confirm -eq "y" -or $confirm -eq "Y") {{
        foreach ($old in $OldVenvs) {{
            $OldPath = Join-Path $ProjectDir $old
            if (Test-Path $OldPath) {{
                Remove-Item -Recurse -Force $OldPath
                Write-Host "   ✓ Удалён $old/" -ForegroundColor Green
            }}
        }}
    }}
}} else {{
    Write-Host "   ✓ Старых окружений не найдено" -ForegroundColor Green
}}

# .env файл
Write-Host ""
$EnvFile = Join-Path $ProjectDir ".env"
$EnvExample = Join-Path $ProjectDir ".env.example"
if ((-not (Test-Path $EnvFile)) -and (Test-Path $EnvExample)) {{
    Write-Host "📝 Создаю .env из .env.example..." -ForegroundColor Yellow
    Copy-Item $EnvExample $EnvFile
    Write-Host "   ✓ .env создан — отредактируй его!" -ForegroundColor Green
}}

# Итоги
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "✅ Bootstrap завершён!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "Следующие шаги:"
Write-Host ""
Write-Host "  1. Активируй окружение:"
Write-Host "     $VenvPath\\Scripts\\Activate.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "  2. Настрой .env:"
Write-Host "     notepad .env" -ForegroundColor Cyan
Write-Host ""
Write-Host "  3. Запусти бота:"
Write-Host "     python bot/main.py" -ForegroundColor Cyan
Write-Host ""
'''

REQUIREMENTS = '''# ═══════════════════════════════════════
# Зависимости — {project_name}
# ═══════════════════════════════════════

# Telegram Bot
aiogram>=3.4

# HTTP
aiohttp>=3.9

# Валидация и настройки
pydantic>=2.6
pydantic-settings>=2.2

# Переменные окружения
python-dotenv>=1.0

# База данных
aiosqlite>=0.20

# Логирование (опционально)
# loguru>=0.7
'''

GITIGNORE = '''# ═══════════════════════════════════════
# Git Ignore — {project_name}
# ═══════════════════════════════════════

# Python
__pycache__/
*.py[cod]
*$py.class
*.pyo
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/
*.egg-info/
dist/
build/

# Виртуальные окружения (на всякий случай)
venv/
.venv/
env/
ENV/

# Логи и данные
logs/
data/
artifacts/
*.log
*.csv
*.sqlite3
*.db

# Секреты
.env
.env.*
!.env.example
*.pem
*.key
*.secret

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Node (если появится)
node_modules/
package-lock.json
'''

ENV_EXAMPLE = '''# ═══════════════════════════════════════
# Переменные окружения — {project_name}
# Скопируй в .env и заполни значения
# ═══════════════════════════════════════

# Telegram Bot
BOT_TOKEN=your_bot_token_here

# База данных
DATABASE_PATH=database/app.sqlite3

# API сервер (если нужен)
API_HOST=0.0.0.0
API_PORT=8000

# Режим отладки
DEBUG=false

# Playwright (если нужен)
# PLAYWRIGHT_BROWSERS_PATH=../_pw-browsers
'''

CONFIG_PY = '''"""
Конфигурация проекта — {project_name}
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # Telegram
    bot_token: str
    
    # База данных
    database_path: Path = Path("database/app.sqlite3")
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Режим отладки
    debug: bool = False


# Глобальный экземпляр настроек
settings = Settings()
'''

BOT_MAIN = '''"""
🤖 Telegram Bot — {project_name}
Точка входа
"""

import asyncio
import logging
import sys
from pathlib import Path

# Добавляем корень проекта в path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import settings
from bot.handlers import start


# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/bot.log", encoding="utf-8"),
    ]
)
logger = logging.getLogger(__name__)


async def main():
    """Запуск бота"""
    
    logger.info("🚀 Запуск бота...")
    
    # Создаём бота и диспетчер
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Подключаем роутеры
    dp.include_router(start.router)
    
    # Запускаем
    try:
        logger.info("✅ Бот запущен!")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("👋 Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
'''

BOT_HANDLERS_START = '''"""
Обработчик /start и /help
"""

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        f"👋 Привет, <b>{{message.from_user.first_name}}</b>!\\n\\n"
        f"Я бот <b>{project_name}</b>.\\n\\n"
        f"Используй /help для списка команд."
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    await message.answer(
        "📚 <b>Доступные команды:</b>\\n\\n"
        "/start — Начать работу\\n"
        "/help — Показать помощь"
    )
'''

BOT_HANDLERS_INIT = '''"""
Handlers package
"""

from bot.handlers import start

__all__ = ["start"]
'''

DATABASE_DB = '''"""
Работа с базой данных
"""

import aiosqlite
from pathlib import Path
from config import settings


async def init_db():
    """Инициализация базы данных"""
    
    # Создаём папку если нет
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    
    async with aiosqlite.connect(settings.database_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def get_user(telegram_id: int):
    """Получить пользователя по telegram_id"""
    async with aiosqlite.connect(settings.database_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,)
        ) as cursor:
            return await cursor.fetchone()


async def create_user(telegram_id: int, username: str = None, first_name: str = None):
    """Создать пользователя"""
    async with aiosqlite.connect(settings.database_path) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (telegram_id, username, first_name) VALUES (?, ?, ?)",
            (telegram_id, username, first_name)
        )
        await db.commit()
'''

WEBAPP_INDEX = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{project_name} — Mini App</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 {project_name}</h1>
            <p class="subtitle">Mini App</p>
        </header>
        
        <main>
            <div class="card">
                <h2>Добро пожаловать!</h2>
                <p>Это твой Mini App. Начни разработку!</p>
            </div>
            
            <div class="user-info" id="userInfo">
                <!-- Заполнится из JS -->
            </div>
        </main>
        
        <footer>
            <button class="btn primary" id="mainBtn">Начать</button>
        </footer>
    </div>
    
    <script src="app.js"></script>
</body>
</html>
'''

WEBAPP_CSS = '''/* ═══════════════════════════════════════
   Стили Mini App — {project_name}
   ═══════════════════════════════════════ */

:root {{
    --tg-theme-bg-color: #ffffff;
    --tg-theme-text-color: #000000;
    --tg-theme-hint-color: #999999;
    --tg-theme-link-color: #2481cc;
    --tg-theme-button-color: #2481cc;
    --tg-theme-button-text-color: #ffffff;
    --tg-theme-secondary-bg-color: #f0f0f0;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    background-color: var(--tg-theme-bg-color);
    color: var(--tg-theme-text-color);
    min-height: 100vh;
    padding: 16px;
}}

.container {{
    max-width: 400px;
    margin: 0 auto;
}}

header {{
    text-align: center;
    margin-bottom: 24px;
}}

header h1 {{
    font-size: 24px;
    margin-bottom: 4px;
}}

.subtitle {{
    color: var(--tg-theme-hint-color);
    font-size: 14px;
}}

.card {{
    background: var(--tg-theme-secondary-bg-color);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}}

.card h2 {{
    font-size: 18px;
    margin-bottom: 8px;
}}

.card p {{
    color: var(--tg-theme-hint-color);
    font-size: 14px;
    line-height: 1.5;
}}

.user-info {{
    background: var(--tg-theme-secondary-bg-color);
    border-radius: 12px;
    padding: 16px;
}}

.btn {{
    width: 100%;
    padding: 14px 24px;
    border: none;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s;
}}

.btn:active {{
    opacity: 0.8;
}}

.btn.primary {{
    background: var(--tg-theme-button-color);
    color: var(--tg-theme-button-text-color);
}}

footer {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 16px;
    background: var(--tg-theme-bg-color);
}}
'''

WEBAPP_JS = '''// ═══════════════════════════════════════
// Mini App JS — {project_name}
// ═══════════════════════════════════════

// Инициализация Telegram Web App
const tg = window.Telegram.WebApp;

// Сообщаем что приложение готово
tg.ready();

// Расширяем на весь экран
tg.expand();

// Получаем данные пользователя
const user = tg.initDataUnsafe?.user;

// Отображаем информацию о пользователе
const userInfoEl = document.getElementById('userInfo');
if (user) {{
    userInfoEl.innerHTML = `
        <h3>👤 Пользователь</h3>
        <p><strong>Имя:</strong> ${{user.first_name}} ${{user.last_name || ''}}</p>
        <p><strong>Username:</strong> @${{user.username || 'не указан'}}</p>
        <p><strong>ID:</strong> ${{user.id}}</p>
    `;
}} else {{
    userInfoEl.innerHTML = '<p>Откройте через Telegram</p>';
}}

// Обработчик кнопки
document.getElementById('mainBtn').addEventListener('click', () => {{
    tg.showAlert('Привет! 👋');
}});

// Main Button (нативная кнопка Telegram)
tg.MainButton.setText('Готово');
tg.MainButton.onClick(() => {{
    tg.close();
}});
// tg.MainButton.show();  // Раскомментируй если нужна
'''

README = '''# 🤖 {project_name}

Telegram бот + Mini App

## 🚀 Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone <repo-url>
cd {project_name}

# 2. Запустить bootstrap
./scripts/bootstrap.sh      # Linux/Mac
.\\scripts\\bootstrap.ps1    # Windows

# 3. Активировать окружение
source ../_venvs/{project_name}-venv/bin/activate      # Linux/Mac
..\_venvs\{project_name}-venv\Scripts\Activate.ps1     # Windows

# 4. Настроить переменные
cp .env.example .env
nano .env  # Заполнить BOT_TOKEN

# 5. Запустить бота
python bot/main.py
```

## 📁 Структура проекта

```
{project_name}/
├── bot/                # Telegram бот
│   ├── handlers/       # Обработчики команд
│   ├── keyboards/      # Клавиатуры
│   ├── utils/          # Утилиты
│   └── main.py         # Точка входа
├── webapp/             # Mini App
├── database/           # База данных
├── api/                # API сервер
├── scripts/            # Скрипты
├── _AI_INCLUDE/        # Документация для AI
├── data/               # Данные (игнорируется)
├── logs/               # Логи (игнорируется)
└── artifacts/          # Временное (игнорируется)
```

## 🐍 Виртуальное окружение

Окружение хранится **вне проекта** в `../_venvs/{project_name}-venv/`

Это сделано чтобы:
- Не раздувать проект (экономия 200-800 MB)
- Cursor не индексировал зависимости
- Легко пересоздать из requirements.txt

## 📚 Документация

Смотри папку `_AI_INCLUDE/`:
- `PROJECT_CONVENTIONS.md` — правила проекта
- `WHERE_THINGS_LIVE.md` — где что лежит
- `DEPENDENCIES.md` — зависимости

## 🛠️ Разработка

```bash
# Добавить пакет
pip install <package>
pip freeze > requirements.txt

# Запустить бота
python bot/main.py

# Смотреть логи
tail -f logs/bot.log
```
'''


# ═══════════════════════════════════════════════════════════════
# ГЕНЕРАТОР
# ═══════════════════════════════════════════════════════════════

def create_file(path: Path, content: str, executable: bool = False):
    """Создать файл с содержимым"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    
    if executable:
        # Делаем исполняемым на Unix
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)
    
    print(f"  ✅ {path}")


def create_project(name: str, base_path: Path):
    """Создать проект"""
    
    import sys
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    date = datetime.now().strftime("%Y-%m-%d")
    
    project_dir = base_path / name
    
    if project_dir.exists():
        print(f"❌ Папка {project_dir} уже существует!")
        return False
    
    print(f"""
═══════════════════════════════════════════════════════════
🚀 Создание проекта: {name}
═══════════════════════════════════════════════════════════
📁 Путь: {project_dir}
🐍 Python: {python_version}
📅 Дата: {date}
═══════════════════════════════════════════════════════════
""")
    
    # Контекст для шаблонов
    ctx = {
        'project_name': name,
        'python_version': python_version,
        'date': date,
    }
    
    # Создаём структуру
    print("📂 Создаю структуру папок...")
    
    dirs = [
        'bot/handlers',
        'bot/keyboards', 
        'bot/utils',
        'bot/middlewares',
        'webapp/assets',
        'scripts',
        'database',
        'api',
        'data',
        'logs',
        'artifacts',
        '_AI_INCLUDE',
    ]
    
    for d in dirs:
        (project_dir / d).mkdir(parents=True, exist_ok=True)
        print(f"  📁 {d}/")
    
    print("\n📄 Создаю файлы...")
    
    # Основные конфиги
    create_file(project_dir / '.cursorignore', CURSORIGNORE.format(**ctx))
    create_file(project_dir / '.cursorrules', CURSORRULES.format(**ctx))
    create_file(project_dir / '.gitignore', GITIGNORE.format(**ctx))
    create_file(project_dir / '.env.example', ENV_EXAMPLE.format(**ctx))
    create_file(project_dir / 'requirements.txt', REQUIREMENTS.format(**ctx))
    create_file(project_dir / 'config.py', CONFIG_PY.format(**ctx))
    create_file(project_dir / 'README.md', README.format(**ctx))
    
    # AI Include
    create_file(project_dir / '_AI_INCLUDE/PROJECT_CONVENTIONS.md', PROJECT_CONVENTIONS.format(**ctx))
    create_file(project_dir / '_AI_INCLUDE/WHERE_THINGS_LIVE.md', WHERE_THINGS_LIVE.format(**ctx))
    create_file(project_dir / '_AI_INCLUDE/DEPENDENCIES.md', DEPENDENCIES.format(**ctx))
    
    # Scripts
    create_file(project_dir / 'scripts/bootstrap.sh', BOOTSTRAP_SH.format(**ctx), executable=True)
    create_file(project_dir / 'scripts/bootstrap.ps1', BOOTSTRAP_PS1.format(**ctx))
    
    # Bot
    create_file(project_dir / 'bot/__init__.py', '"""Bot package"""')
    create_file(project_dir / 'bot/main.py', BOT_MAIN.format(**ctx))
    create_file(project_dir / 'bot/handlers/__init__.py', BOT_HANDLERS_INIT.format(**ctx))
    create_file(project_dir / 'bot/handlers/start.py', BOT_HANDLERS_START.format(**ctx))
    create_file(project_dir / 'bot/keyboards/__init__.py', '"""Keyboards package"""')
    create_file(project_dir / 'bot/utils/__init__.py', '"""Utils package"""')
    create_file(project_dir / 'bot/middlewares/__init__.py', '"""Middlewares package"""')
    
    # Database
    create_file(project_dir / 'database/__init__.py', '"""Database package"""')
    create_file(project_dir / 'database/db.py', DATABASE_DB.format(**ctx))
    
    # API
    create_file(project_dir / 'api/__init__.py', '"""API package"""')
    create_file(project_dir / 'api/server.py', '"""API Server — TODO"""')
    
    # Webapp
    create_file(project_dir / 'webapp/index.html', WEBAPP_INDEX.format(**ctx))
    create_file(project_dir / 'webapp/styles.css', WEBAPP_CSS.format(**ctx))
    create_file(project_dir / 'webapp/app.js', WEBAPP_JS.format(**ctx))
    
    # .gitkeep для пустых папок
    create_file(project_dir / 'data/.gitkeep', '')
    create_file(project_dir / 'logs/.gitkeep', '')
    create_file(project_dir / 'artifacts/.gitkeep', '')
    create_file(project_dir / 'webapp/assets/.gitkeep', '')
    
    # Итоги
    print(f"""
═══════════════════════════════════════════════════════════
✅ Проект создан!
═══════════════════════════════════════════════════════════

Следующие шаги:

  1. Перейди в проект:
     cd {project_dir}

  2. Запусти bootstrap:
     ./scripts/bootstrap.sh      # Linux/Mac
     .\\scripts\\bootstrap.ps1    # Windows

  3. Активируй окружение:
     source ../_venvs/{name}-venv/bin/activate

  4. Настрой .env:
     cp .env.example .env
     nano .env

  5. Запусти бота:
     python bot/main.py

═══════════════════════════════════════════════════════════
""")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='🚀 Генератор проекта: Telegram Bot + Mini App',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры:
  python create_project.py my_bot
  python create_project.py awesome_bot --path ~/projects
        '''
    )
    
    parser.add_argument('name', help='Название проекта (латиница, без пробелов)')
    parser.add_argument('--path', default='.', help='Путь где создать проект (по умолчанию: текущая папка)')
    
    args = parser.parse_args()
    
    # Валидация имени
    if not args.name.replace('_', '').replace('-', '').isalnum():
        print("❌ Название должно содержать только буквы, цифры, _ и -")
        return
    
    base_path = Path(args.path).resolve()
    
    if not base_path.exists():
        print(f"❌ Путь {base_path} не существует!")
        return
    
    create_project(args.name, base_path)


if __name__ == '__main__':
    main()


## 🚀 Как использовать

### Установка (один раз)

#bash
# Сохрани скрипт в удобное место
# mkdir -p ~/scripts
# Скопируй код выше в ~/scripts/create_project.py

# Сделай исполняемым (Linux/Mac)
#chmod +x ~/scripts/create_project.py

# Добавь алиас (опционально)
#echo 'alias newbot="python ~/scripts/create_project.py"' >> ~/.bashrc
#source ~/.bashrc


### Создание проекта

#bash
# Вариант 1: Полный путь
#python ~/scripts/create_project.py my_awesome_bot

# Вариант 2: С алиасом
#newbot my_awesome_bot

# Вариант 3: В конкретную папку
#python ~/scripts/create_project.py my_bot --path ~/projects


### Результат за 1 команду


#═══════════════════════════════════════════════════════════
#🚀 Создание проекта: my_awesome_bot
#═══════════════════════════════════════════════════════════

#📂 Создаю структуру папок...
 # 📁 bot/handlers/
  #📁 bot/keyboards/
  #📁 webapp/assets/
 # ...

#📄 Создаю файлы...
  #✅ .cursorignore
  #✅ .cursorrules
  #✅ _AI_INCLUDE/PROJECT_CONVENTIONS.md
  #✅ bot/main.py
  #✅ webapp/index.html
#  ...

#═══════════════════════════════════════════════════════════
#✅ Проект создан!
#═══════════════════════════════════════════════════════════




## 📊 Что создаётся

# Файл/Папка | Назначение |
#------------|------------|
# `.cursorignore` | Исключения для Cursor |
## `.cursorrules` | Правила для AI |
#`_AI_INCLUDE/` | Документация для AI |
# `bot/` | Готовый бот с handlers |
# `webapp/` | Mini App с Telegram SDK |
#`database/` | Работа с SQLite |
# `scripts/bootstrap.sh` | Создание venv |
#`requirements.txt` | Зависимости |
#`.env.example` | Пример переменных |



## 🎯 Итог

#**1 команда = полный проект за 5 секунд:**
#- ✅ Правильная структура
#- ✅ venv вне проекта
#- ✅ Cursor не жрёт токены
#- ✅ AI знает правила
#- ✅ Готовый бот
#- ✅ Готовый Mini App
#- ✅ База данных
#- ✅ Bootstrap скрипт
