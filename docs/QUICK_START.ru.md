# ⚡ Быстрый старт

Создай первый проект за 2 минуты!

> 🇬🇧 [English version](QUICK_START.md)

---

## 1️⃣ Установка

```bash
pip install ai-toolkit
```

---

## 2️⃣ Создание проекта

**Вариант A: Web Dashboard**
```bash
ai-toolkit dashboard
```

**Вариант B: Одна команда**
```bash
ai-toolkit create my_bot --template bot
```

**Вариант C: Интерактивный режим**
```bash
ai-toolkit
```

---

## 3️⃣ Настройка

```bash
cd my_bot

# Создать venv (вне проекта!)
./scripts/bootstrap.sh

# Активировать
source ../_venvs/my_bot-venv/bin/activate

# Настроить .env
cp .env.example .env
```

---

## 4️⃣ Запуск

```bash
python main.py
```

---

## 🎉 Готово!

### Что дальше?

- 📖 [Полное руководство](GUIDE.ru.md) — подробная документация
- ❓ [FAQ](FAQ.ru.md) — частые вопросы
- 🐙 [GitHub](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding) — поставь звезду ⭐
- 📱 [Telegram](https://t.me/MichaelSalmin) — получить помощь

---

## 📦 Доступные шаблоны

| Команда | Описание |
|---------|----------|
| `--template bot` | Telegram Бот (aiogram) |
| `--template webapp` | Mini App (HTML/JS) |
| `--template fastapi` | REST API |
| `--template parser` | Web Парсер |
| `--template full` | Все модули |
| `--template monorepo` | Мульти-проект |

---

## 🛠️ Полезные команды

```bash
# Очистить грязный проект
ai-toolkit cleanup ./my_project --level medium

# Health check
ai-toolkit health ./my_project

# Добавить toolkit в существующий проект
ai-toolkit migrate ./my_project

# Открыть Web Dashboard
ai-toolkit dashboard
```

---

## 🖥️ Выбор IDE

При создании проекта выбери свою IDE:

| IDE | Создаваемые файлы |
|-----|-------------------|
| 💜 Cursor | `.cursorrules`, `.cursorignore` |
| 💙 Copilot | `.github/copilot-instructions.md` |
| 🟢 Claude | `CLAUDE.md` |
| 🌊 Windsurf | `.windsurfrules` |
| 🔄 Все | Все файлы |

