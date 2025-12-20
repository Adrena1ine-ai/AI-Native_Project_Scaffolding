# 📖 Полное руководство по AI Toolkit

Это руководство поможет тебе освоить AI Toolkit от начала до конца.

> 🇬🇧 [English version](GUIDE.md)

---

## 📋 Содержание

1. [Введение](#введение)
2. [Установка](#установка)
3. [Первый проект](#первый-проект)
4. [Интерфейсы](#интерфейсы)
5. [Шаблоны проектов](#шаблоны-проектов)
6. [Работа с venv](#работа-с-venv)
7. [AI конфигурация](#ai-конфигурация)
8. [Context Switcher](#context-switcher)
9. [Очистка проектов](#очистка-проектов)
10. [Миграция](#миграция)
11. [Docker и CI/CD](#docker-и-cicd)
12. [Плагины](#плагины)
13. [Troubleshooting](#troubleshooting)

---

## Введение

### Что такое AI Toolkit?

AI Toolkit — это инструмент для создания Python-проектов, оптимизированных для работы с AI-ассистентами (Cursor, GitHub Copilot, Claude, Windsurf).

### Зачем это нужно?

Когда AI-ассистент работает с проектом, он читает ВСЕ файлы. Если `venv/` находится внутри проекта:

- 📦 AI индексирует 500+ MB зависимостей
- 🐌 IDE тормозит
- 🤯 AI путается, читая код из библиотек
- 💾 Репозиторий раздувается

**Решение:** AI Toolkit создаёт проекты с venv ВНЕ проекта и специальными конфигами для AI.

---

## Установка

### Требования

- Python 3.10 или выше
- pip

### Через pip (рекомендуется)

```bash
pip install ai-toolkit
```

### Из исходников

```bash
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding
pip install -e .
```

### Проверка установки

```bash
ai-toolkit --version
```

---

## Первый проект

### Интерактивный режим

```bash
ai-toolkit
```

1. Выбери язык (🇬🇧 English / 🇷🇺 Русский)
2. Выбери IDE
3. Выбери "Создать новый проект"
4. Введи название проекта
5. Выбери шаблон
6. Готово! 🎉

### CLI режим

```bash
ai-toolkit create my_bot --template bot --path ~/projects
```

### После создания

```bash
cd ~/projects/my_bot
./scripts/bootstrap.sh
source ../_venvs/my_bot-venv/bin/activate
cp .env.example .env
```

---

## Интерфейсы

### CLI (Командная строка)

```bash
# Интерактивный режим
ai-toolkit

# Создать проект
ai-toolkit create my_bot

# Очистка
ai-toolkit cleanup ./my_project --level medium

# Health check
ai-toolkit health ./my_project
```

### Web Dashboard

```bash
ai-toolkit dashboard
# или
ai-toolkit web
```

Откроется красивый веб-интерфейс на http://127.0.0.1:8080

### GUI (Tkinter)

```bash
python -m gui.app
```

---

## Шаблоны проектов

| Шаблон | Описание | Включает |
|--------|----------|----------|
| `bot` | Telegram Бот | aiogram 3.x, handlers, FSM |
| `webapp` | Telegram Mini App | HTML/CSS/JS, Telegram Web App API |
| `fastapi` | REST API | FastAPI, Pydantic, async |
| `parser` | Web Парсер | aiohttp, BeautifulSoup |
| `full` | Все модули | bot + webapp + parser + API |
| `monorepo` | Мульти-проект | Общие библиотеки, несколько сервисов |

### Выбор шаблона

```bash
# CLI
ai-toolkit create my_project --template fastapi

# Интерактивно - выбери из меню
```

---

## Работа с venv

### Почему venv снаружи?

```
projects/
├── _venvs/                 ← Все venv здесь!
│   ├── bot1-venv/
│   ├── bot2-venv/
│   └── api-venv/
│
├── bot1/                   ← Чистый проект!
├── bot2/
└── api/
```

**Преимущества:**

- ✅ AI видит только твой код
- ✅ IDE работает быстро
- ✅ Репозиторий лёгкий
- ✅ Легко удалить/пересоздать venv

### bootstrap.sh

Скрипт `scripts/bootstrap.sh` создаёт venv вне проекта:

```bash
./scripts/bootstrap.sh
```

Что делает:

1. Создаёт `../_venvs/project-name-venv/`
2. Устанавливает зависимости из `requirements.txt`
3. Показывает команду активации

### Активация

```bash
# Linux/macOS
source ../_venvs/my_project-venv/bin/activate

# Windows
..\_venvs\my_project-venv\Scripts\activate
```

---

## AI конфигурация

### Файлы для каждой IDE

| IDE | Файлы |
|-----|-------|
| 💜 Cursor | `.cursorrules`, `.cursorignore` |
| 💙 GitHub Copilot | `.github/copilot-instructions.md` |
| 🟢 Claude | `CLAUDE.md` |
| 🌊 Windsurf | `.windsurfrules` |

### Папка _AI_INCLUDE

```
_AI_INCLUDE/
├── PROJECT_CONVENTIONS.md  # Правила: что AI может/не может
└── WHERE_IS_WHAT.md        # Архитектура: где что искать
```

**AI читает эти файлы ПЕРВЫМИ** и следует правилам.

---

## Context Switcher

Когда AI тупит на большом проекте — скрой ненужные модули!

### Использование

```bash
# Показать справку
python scripts/context.py

# Скрыть модуль от AI
python scripts/context.py hide parser

# Показать модуль
python scripts/context.py show parser

# Список скрытых
python scripts/context.py list
```

### Как работает

Скрипт переименовывает папки в `_hidden_module_name`. Cursor/Copilot игнорируют файлы начинающиеся с `_`.

---

## Очистка проектов

### Уровни очистки

| Уровень | Действия |
|---------|----------|
| `safe` | Только анализ, без изменений |
| `medium` | Бэкап + перенос venv + создание конфигов |
| `full` | + перенос данных + реструктуризация |

### CLI

```bash
# Только анализ
ai-toolkit cleanup ./my_project --level safe

# Перенос venv + конфиги
ai-toolkit cleanup ./my_project --level medium
```

### Что проверяется

- ❌ venv внутри проекта
- ❌ site-packages в репо
- ⚠️ Большие логи (>10MB)
- ⚠️ Большая папка data
- ⚠️ Папки __pycache__
- ⚠️ Отсутствие AI конфигов

---

## Миграция

Добавление AI Toolkit в существующий проект:

```bash
ai-toolkit migrate ./my_old_project
```

### Что добавляется

- Папка `_AI_INCLUDE/`
- `.cursorrules`, `.cursorignore`
- `CLAUDE.md`
- `scripts/bootstrap.sh`
- `scripts/context.py`
- `.toolkit-version`

---

## Docker и CI/CD

### Docker

```dockerfile
# Dockerfile создаётся автоматически
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]
```

```bash
# Сборка и запуск
docker-compose up --build
```

### GitHub Actions

**CI (ci.yml):**

- Linting (ruff)
- Type checking (mypy)
- Tests (pytest)

**CD (cd.yml):**

- Build при push тега
- Деплой на продакшен

### Dependabot

Автообновление зависимостей еженедельно.

---

## Плагины

### Структура плагина

```
~/.ai_toolkit/plugins/
└── my_plugin/
    ├── __init__.py
    └── plugin.py
```

### plugin.py

```python
def on_project_created(project_path: str, template: str) -> None:
    """Вызывается после создания проекта."""
    print(f"Проект создан: {project_path}")

def on_cleanup(project_path: str, level: str) -> None:
    """Вызывается после очистки."""
    pass
```

---

## Troubleshooting

### venv не активируется

```bash
# Проверь существует ли venv
ls ../_venvs/

# Пересоздай
rm -rf ../_venvs/my_project-venv
./scripts/bootstrap.sh
```

### AI всё ещё индексирует venv

1. Проверь что `.cursorignore` существует
2. Перезапусти IDE
3. Очисти кеш IDE

### Dashboard не запускается

```bash
# Установи зависимости
pip install fastapi uvicorn jinja2 python-multipart

# Запусти вручную
python -m web.app
```

### Ошибки "Module not found"

```bash
# Проверь что venv активирован
which python
# Должен показать: ../_venvs/my_project-venv/bin/python

# Переустанови зависимости
pip install -r requirements.txt
```

---

## Поддержка

- 📱 Telegram: [@MichaelSalmin](https://t.me/MichaelSalmin)
- 🐙 GitHub Issues: [Сообщить об ошибке](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/issues)
- 💬 Discussions: [Задать вопрос](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/discussions)

