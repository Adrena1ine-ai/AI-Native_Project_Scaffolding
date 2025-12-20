# 🛠️ AI Toolkit v3.0

> Создавай AI-friendly проекты за секунды

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Что это?

**AI Toolkit** — инструмент который создаёт проекты, оптимизированные для работы с AI-ассистентами (Cursor, GitHub Copilot, Claude, Windsurf).

### Проблема

AI-ассистенты создают `venv/` внутри проекта → 500MB мусора → IDE тормозит → AI тупит.

### Решение

AI Toolkit создаёт проекты с правильной структурой и защитой от загрязнения.

---

## 🚀 Быстрый старт

```bash
# Распаковать
tar -xzf ai_toolkit_v3.tar.gz
cd ai_toolkit

# Установить зависимость
pip install pyyaml

# Запустить
python __main__.py
```

---

## 💻 Использование

### Интерактивный режим

```bash
python __main__.py
```

```
═══════════════════════════════════════════════════════════
🛠️  AI TOOLKIT v3.0.0
═══════════════════════════════════════════════════════════

🖥️  В какой IDE будешь работать?

  1. 💜 Cursor (AI-first IDE)
  2. 💙 VS Code + GitHub Copilot
  3. 🟢 VS Code + Claude
  4. 🌊 Windsurf
  5. 🔄 Все сразу (универсальный)

Выбери (1-5):
```

### CLI режим

```bash
# Создать проект
python __main__.py create my_bot --template bot --ai copilot

# Очистить грязный проект
python __main__.py cleanup ./old_project --level medium

# Health check
python __main__.py health ./my_project

# Миграция
python __main__.py migrate ./existing_project

# Обновление
python __main__.py update ./my_project
```

---

## 📦 Шаблоны

| Шаблон | Описание |
|--------|----------|
| `bot` | Telegram бот (aiogram 3.x) |
| `webapp` | Telegram Mini App |
| `fastapi` | REST API |
| `parser` | Web парсер |
| `full` | Всё вместе |
| `monorepo` | Несколько проектов |

---

## 🤖 Поддержка AI

| IDE | Файлы |
|-----|-------|
| Cursor | `.cursorrules`, `.cursorignore` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude | `CLAUDE.md` |
| Windsurf | `.windsurfrules` |

---

## 🛡️ Функции

| Функция | Описание |
|---------|----------|
| **Создание** | Готовая структура проекта |
| **Очистка** | Анализ + перенос venv + создание конфигов |
| **Миграция** | Добавить Toolkit в существующий проект |
| **Health check** | Проверка правильности настройки |
| **Docker** | Dockerfile + docker-compose |
| **CI/CD** | GitHub Actions |
| **Git** | Автоматический git init + первый коммит |
| **pre-commit** | Хуки для защиты от venv в проекте |
| **Context Switcher** | Скрыть модули от AI |

---

## 📁 Структура созданного проекта

```
my_project/
├── _AI_INCLUDE/              # Правила для AI
│   ├── PROJECT_CONVENTIONS.md
│   └── WHERE_IS_WHAT.md
├── .cursorrules              # Cursor
├── .cursorignore
├── .github/
│   ├── copilot-instructions.md
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── CLAUDE.md
├── scripts/
│   ├── bootstrap.sh          # Создаёт venv ВНЕ проекта
│   ├── health_check.sh
│   └── context.py            # Context Switcher
├── bot/
│   ├── main.py
│   └── handlers/
├── database/
├── logs/
├── data/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🎮 Context Switcher

Если AI тупит на большом проекте:

```bash
python scripts/context.py bot     # Фокус на bot/
python scripts/context.py webapp  # Фокус на webapp/
python scripts/context.py all     # Видит всё
```

---

## 🧹 Уровни очистки

| Уровень | Действия |
|---------|----------|
| `safe` | Только анализ |
| `medium` | Бэкап + перенос venv + создание конфигов |
| `full` | + перенос данных + реструктуризация |

---

## 📋 TODO

- [ ] GUI (Tkinter/PyQt)
- [ ] Шаблоны в отдельных файлах
- [ ] Система плагинов
- [ ] Публикация на PyPI
- [ ] Monorepo поддержка

---

## 📄 License

MIT
